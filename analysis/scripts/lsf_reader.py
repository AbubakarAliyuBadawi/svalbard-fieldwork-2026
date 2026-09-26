"""
Self-contained LSF (LSTS log file) reader driven by the IMC.xml shipped with each log.

An LSF file is a flat concatenation of IMC messages:

    header  : sync(u16) mgid(u16) size(u16) timestamp(f64) src(u16) src_ent(u8) dst(u16) dst_ent(u8)   [20 bytes]
    payload : `size` bytes, field layout given by IMC.xml
    footer  : crc16(u16)  CRC-16-IBM over header+payload

Byte order is detected from the sync word (0xFE54 / 0xFE55 depending on IMC version, taken
from the <header> block of IMC.xml). If the two sync bytes appear swapped, the message is
big-endian.

Variable-length field types:
    plaintext / rawdata : u16 length + bytes
    message             : u16 message id (0xFFFF = null) + inline payload (no header/footer)
    message-list        : u16 count, then `count` inline messages (each: u16 id + payload)

Only messages whose abbrev is in `wanted` are decoded; everything else is skipped by seeking,
so sonar payloads cost nothing.  Nothing is filtered or resampled here.
"""
from __future__ import annotations

import gzip
import struct
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

HEADER_FMT = "HHHdHBHB"          # 20 bytes
HEADER_SIZE = struct.calcsize("<" + HEADER_FMT)

PRIM = {
    "int8_t": "b", "uint8_t": "B", "int16_t": "h", "uint16_t": "H",
    "int32_t": "i", "uint32_t": "I", "int64_t": "q", "fp32_t": "f", "fp64_t": "d",
}


@dataclass
class Field:
    abbrev: str
    type: str
    msg_type: str | None = None   # for message / message-list


@dataclass
class MsgDef:
    id: int
    abbrev: str
    fields: list[Field] = field(default_factory=list)
    fixed_fmt: str | None = None  # struct format if all fields primitive


class IMCDefs:
    """Parses IMC.xml(.gz) into message definitions."""

    def __init__(self, xml_path: str | Path):
        xml_path = Path(xml_path)
        raw = gzip.open(xml_path, "rb").read() if xml_path.suffix == ".gz" else xml_path.read_bytes()
        root = ET.fromstring(raw)
        self.version = root.attrib.get("version", "?")
        sync_el = root.find("./header/field[@abbrev='sync']")
        self.sync = int(sync_el.attrib["value"], 16) if sync_el is not None else 0xFE54
        self.by_id: dict[int, MsgDef] = {}
        self.by_abbrev: dict[str, MsgDef] = {}
        for m in root.findall("message"):
            md = MsgDef(int(m.attrib["id"]), m.attrib["abbrev"])
            for f in m.findall("field"):
                md.fields.append(Field(f.attrib["abbrev"], f.attrib["type"],
                                       f.attrib.get("message-type")))
            if all(f.type in PRIM for f in md.fields):
                md.fixed_fmt = "".join(PRIM[f.type] for f in md.fields)
            self.by_id[md.id] = md
            self.by_abbrev[md.abbrev] = md
        # enumerations for a few fields we report (VehicleMedium etc.)
        self.enums: dict[tuple[str, str], dict[int, str]] = {}
        for m in root.findall("message"):
            for f in m.findall("field"):
                vals = f.findall("value")
                if vals and f.attrib.get("unit") in ("Enumerated", "Bitfield"):
                    self.enums[(m.attrib["abbrev"], f.attrib["abbrev"])] = {
                        int(v.attrib["id"], 0): v.attrib["abbrev"] for v in vals}


# ---------------------------------------------------------------------------
# CRC-16-IBM (poly 0x8005, reflected 0xA001, init 0)
# ---------------------------------------------------------------------------
_CRC_TABLE = []
for _i in range(256):
    _c = _i
    for _ in range(8):
        _c = (_c >> 1) ^ 0xA001 if _c & 1 else _c >> 1
    _CRC_TABLE.append(_c)


def crc16(data: bytes | memoryview) -> int:
    c = 0
    t = _CRC_TABLE
    for b in data:
        c = (c >> 8) ^ t[(c ^ b) & 0xFF]
    return c


# ---------------------------------------------------------------------------
# Payload decoding
# ---------------------------------------------------------------------------
class Decoder:
    def __init__(self, defs: IMCDefs, endian: str):
        self.defs = defs
        self.e = endian
        self._fixed = {mid: struct.Struct(endian + md.fixed_fmt)
                       for mid, md in defs.by_id.items() if md.fixed_fmt is not None}
        self._u16 = struct.Struct(endian + "H")
        self._prim = {k: struct.Struct(endian + v) for k, v in PRIM.items()}

    def decode(self, mid: int, buf: memoryview, off: int, end: int) -> dict:
        md = self.defs.by_id.get(mid)
        if md is None:
            return {"_raw": bytes(buf[off:end])}
        s = self._fixed.get(mid)
        if s is not None:
            return dict(zip((f.abbrev for f in md.fields), s.unpack_from(buf, off)))
        out, _ = self._decode_generic(md, buf, off)
        return out

    def _decode_generic(self, md: MsgDef, buf: memoryview, off: int):
        out = {}
        for f in md.fields:
            t = f.type
            if t in PRIM:
                st = self._prim[t]
                out[f.abbrev] = st.unpack_from(buf, off)[0]
                off += st.size
            elif t in ("plaintext", "rawdata"):
                n = self._u16.unpack_from(buf, off)[0]
                off += 2
                b = bytes(buf[off:off + n])
                off += n
                out[f.abbrev] = b.decode("utf-8", "replace") if t == "plaintext" else b.hex()
            elif t == "message":
                sub_id = self._u16.unpack_from(buf, off)[0]
                off += 2
                if sub_id == 0xFFFF:
                    out[f.abbrev] = None
                else:
                    sub = self.defs.by_id.get(sub_id)
                    if sub is None:
                        raise ValueError(f"unknown inline message id {sub_id}")
                    val, off = self._decode_generic(sub, buf, off)
                    val["_abbrev"] = sub.abbrev
                    out[f.abbrev] = val
            elif t == "message-list":
                n = self._u16.unpack_from(buf, off)[0]
                off += 2
                lst = []
                for _ in range(n):
                    sub_id = self._u16.unpack_from(buf, off)[0]
                    off += 2
                    if sub_id == 0xFFFF:
                        lst.append(None)
                        continue
                    sub = self.defs.by_id[sub_id]
                    val, off = self._decode_generic(sub, buf, off)
                    val["_abbrev"] = sub.abbrev
                    lst.append(val)
                out[f.abbrev] = lst
            else:
                raise ValueError(f"unhandled type {t}")
        return out, off


# ---------------------------------------------------------------------------
# File reader
# ---------------------------------------------------------------------------
def load_bytes(path: str | Path) -> bytes:
    path = Path(path)
    if path.suffix == ".gz":
        with gzip.open(path, "rb") as fh:
            return fh.read()
    return path.read_bytes()


@dataclass
class ReadResult:
    counts: Counter                       # abbrev -> count
    counts_by_entity: Counter             # (abbrev, src_ent) -> count
    first_ts: dict                        # abbrev -> first timestamp
    last_ts: dict                         # abbrev -> last timestamp
    tables: dict                          # abbrev -> DataFrame (only wanted)
    entities: dict                        # ent id -> label
    t_start: float
    t_end: float
    n_messages: int
    endian: str
    crc_checked: int
    crc_failed: int
    sources: Counter                      # src address -> count


def read_lsf(path: str | Path, defs: IMCDefs, wanted: set[str] | None = None,
             crc_sample: int = 5000, progress: bool = True) -> ReadResult:
    data = load_bytes(path)
    buf = memoryview(data)
    n = len(data)

    # endianness from the first sync word
    sync_le = struct.unpack_from("<H", buf, 0)[0]
    if sync_le == defs.sync:
        endian = "<"
    elif struct.unpack_from(">H", buf, 0)[0] == defs.sync:
        endian = ">"
    else:
        raise ValueError(f"first two bytes {data[:2].hex()} do not match sync 0x{defs.sync:04X}")
    hdr = struct.Struct(endian + HEADER_FMT)
    dec = Decoder(defs, endian)

    wanted_ids = None
    if wanted is not None:
        wanted_ids = {defs.by_abbrev[a].id for a in wanted if a in defs.by_abbrev}
        missing = [a for a in wanted if a not in defs.by_abbrev]
        if missing:
            print(f"  note: not defined in this IMC version, skipped: {missing}")

    counts = Counter()
    counts_by_entity = Counter()
    sources = Counter()
    first_ts, last_ts = {}, {}
    rows = defaultdict(list)
    entities = {}
    off = 0
    n_msg = 0
    crc_checked = crc_failed = 0
    t_start = t_end = None
    rng = np.random.default_rng(0)
    while off + HEADER_SIZE <= n:
        sync, mid, size, ts, src, src_ent, dst, dst_ent = hdr.unpack_from(buf, off)
        if sync != defs.sync:
            # try the other endianness once; otherwise stop (corrupt tail)
            raise ValueError(f"sync mismatch at offset {off}: 0x{sync:04X}")
        p0 = off + HEADER_SIZE
        p1 = p0 + size
        if p1 + 2 > n:
            print(f"  truncated message at offset {off}, stopping")
            break
        md = defs.by_id.get(mid)
        ab = md.abbrev if md else f"id{mid}"
        counts[ab] += 1
        counts_by_entity[(ab, src_ent)] += 1
        sources[src] += 1
        if ab not in first_ts:
            first_ts[ab] = ts
        last_ts[ab] = ts
        if t_start is None:
            t_start = ts
        t_end = ts
        n_msg += 1
        # CRC on a sample of messages (full check would be slow in pure Python)
        if crc_sample and (n_msg <= crc_sample or rng.random() < 0.002):
            crc_checked += 1
            if crc16(buf[off:p1]) != struct.unpack_from(endian + "H", buf, p1)[0]:
                crc_failed += 1
        if mid == 3:  # EntityInfo
            d = dec.decode(mid, buf, p0, p1)
            entities[d["id"]] = d["label"]
        if wanted_ids is None or mid in wanted_ids:
            d = dec.decode(mid, buf, p0, p1)
            d["timestamp"] = ts
            d["src"] = src
            d["src_ent"] = src_ent
            d["dst"] = dst
            d["dst_ent"] = dst_ent
            rows[ab].append(d)
        off = p1 + 2
        if progress and n_msg % 500000 == 0:
            print(f"  {n_msg} messages, {off/n*100:.0f}%")
    tables = {}
    for ab, lst in rows.items():
        df = pd.DataFrame(lst)
        # move bookkeeping columns first
        lead = ["timestamp", "src", "src_ent", "dst", "dst_ent"]
        df = df[lead + [c for c in df.columns if c not in lead]]
        df.insert(3, "src_ent_label", df["src_ent"].map(entities).fillna("?"))
        tables[ab] = df
    return ReadResult(counts, counts_by_entity, first_ts, last_ts, tables, entities,
                      t_start, t_end, n_msg, endian, crc_checked, crc_failed, sources)
