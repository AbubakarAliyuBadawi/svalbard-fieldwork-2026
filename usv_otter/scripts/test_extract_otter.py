"""Checks for navigation integrity and binary framing (no synthetic report data)."""
import tempfile
from pathlib import Path
import struct
import unittest

import numpy as np
import pandas as pd

from extract_otter import align_gps, degrees, nmea_sentences, records


class ExtractionTests(unittest.TestCase):
    def test_hemispheres(self):
        self.assertAlmostEqual(degrees('7825.68994', 'N'), 78.4281656667)
        self.assertAlmostEqual(degrees('01707.64677', 'W'), -17.1274461667)

    def test_checksum(self):
        body = b'GNRMC,143302.20,A,7825.68994,N,01707.64677,E,0.358,273.06,060926,,,D'
        self.assertEqual(len(list(nmea_sentences(b'$' + body + b'*72'))), 1)
        self.assertEqual(len(list(nmea_sentences(b'$' + body + b'*00'))), 0)

    def test_no_interpolation_across_gaps_or_invalid_fixes(self):
        gps = pd.DataFrame(dict(recorder_seconds=[0., 1., 5., 6.], gps_utc_seconds=[100., 101., 105., 106.],
                                latitude=[78., 78.1, 78.5, 78.6], longitude=[17., 17.1, 17.5, 17.6],
                                gps_valid=[True, True, True, False]))
        result = align_gps(np.array([-.1, 0., .5, 3., 5., 5.5, 6.1]), gps)
        np.testing.assert_array_equal(result['gps_valid'], [False, True, True, False, True, False, False])
        self.assertAlmostEqual(result['latitude'][2], 78.05)

    def test_truncation_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sample.dt4'
            path.write_bytes(struct.pack('<HH', 4, 15) + b'12')
            with self.assertRaises(ValueError):
                list(records(path))


if __name__ == '__main__':
    unittest.main()
