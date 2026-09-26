"""
Shared configuration for the amortized-inference pipeline (self-contained; nothing is imported
from other projects). All paths are relative to the analysis/ folder.
"""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]          # field_work_data
ANALYSIS = ROOT / "analysis"
SBI = ANALYSIS / "sbi"
DATA = SBI / "data"
MODELS = SBI / "models"
PLOTS = SBI / "plots"
RESULTS = SBI / "results"
for p in (DATA, MODELS, PLOTS, RESULTS):
    p.mkdir(parents=True, exist_ok=True)

# ---- observation window --------------------------------------------------
T = 120                    # seconds, at 1 Hz
CHANNELS = ["cos_psi", "sin_psi", "wt_u", "wt_v", "rpm_k", "gps_vn", "gps_ve",
            "m_dvl", "m_gps", "bt_u", "bt_v", "m_bt"]
C = len(CHANNELS)

# ---- parameters ------------------------------------------------------------
THETA = ["delta_deg", "scale", "c_n", "c_e", "log10_sigma_v"]
PRIOR_LO = np.array([-15.0, 0.80, -0.40, -0.40, np.log10(0.05)])
PRIOR_HI = np.array([ 15.0, 1.10,  0.40,  0.40, np.log10(0.50)])

# ---- fixed nuisance / noise settings of the simulator (measured on the logs) ----------
RPM_K_RANGE = (0.95e-3, 1.35e-3)   # true m/s per rpm, sampled per window, not inferred
HEADING_NOISE_DEG = 0.3            # AHRS yaw noise (1 Hz mean)
GPS_VEL_NOISE = 0.05               # m/s, receiver SOG/COG at 1 Hz
BT_NOISE_FACTOR = 0.5              # bottom-track noise relative to sigma_v
SWAY_SD = 0.03                     # m/s, AR(1) sway of the true velocity
P_DROP_RANGE = (0.0, 0.08)         # DVL dropout probability per second
P_BT_AVAILABLE = 0.7               # windows with bottom track
P_GPS_AVAILABLE = 0.6              # windows with GPS (surface); the rest are 'submerged'

LOGS = {
    "star": "101134_20260907_star",
    "sidescan": "074948_08_09_sidescan",
    "thor": "094605_0700926LongYoYo1",
}
