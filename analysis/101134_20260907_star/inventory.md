# Inventory: 101134_20260907_star

Source: `101134_20260907_star/Data.lsf.gz` (16.0 MB gz), IMC 5.5.4.9, sync 0xFE55, byte order little-endian.

Messages: 789531. CRC-16 checked on 6583 sampled messages, 0 failures.

## Vehicle identity

- Config.ini `Vehicle =` : **lauv-marie**
- Announce sys_name (own system, src 8259): **['lauv-marie']**
- LoggingControl label: `20260907/101134_20260907_star`
- IMC source addresses seen: {8259: 789088, 16641: 171, 18469: 161, 21108: 87, 32932: 19, 0: 5} (8259 = the vehicle itself)

## Time span (header timestamps, vehicle clock)

- start: 1788775894.983 = 2026-09-07 10:11:34.982Z
- end:   1788776684.983 = 2026-09-07 10:24:44.983Z
- duration: 790.0 s = 13.17 min

## Clock check: header timestamp minus GPS UTC time of fix (s)

| entity | n | median | mean | std | min | max |
|---|---|---|---|---|---|---|
| GPS | 790 | +0.316 | +0.319 | 0.020 | +0.232 | +0.456 |
| Navigation | 1 | +0.325 | +0.325 | nan | +0.325 | +0.325 |

## Message types (count, mean rate over the log, first/last time)

| message | count | rate [Hz] | first | last | decoded |
|---|---|---|---|---|---|
| ControlParcel | 70686 | 89.476 | 10:11:35.041 | 10:24:44.975 |  |
| SetServoPosition | 62792 | 79.484 | 10:11:39.981 | 10:24:44.975 |  |
| Current | 61850 | 78.291 | 10:11:34.985 | 10:24:44.926 |  |
| EntityState | 48507 | 61.401 | 10:11:35.026 | 10:24:44.980 |  |
| CpuUsage | 44175 | 55.918 | 10:11:35.576 | 10:24:44.240 |  |
| EulerAngles | 39499 | 49.999 | 10:11:34.997 | 10:24:44.964 | yes |
| Acceleration | 39499 | 49.999 | 10:11:34.997 | 10:24:44.964 | yes |
| AngularVelocity | 39499 | 49.999 | 10:11:34.997 | 10:24:44.964 | yes |
| MagneticField | 39499 | 49.999 | 10:11:34.997 | 10:24:44.964 | yes |
| ServoPosition | 31592 | 39.990 | 10:11:35.041 | 10:24:44.926 |  |
| Voltage | 30642 | 38.787 | 10:11:34.985 | 10:24:44.906 |  |
| Temperature | 25017 | 31.667 | 10:11:35.037 | 10:24:44.865 | yes |
| Distance | 19750 | 25.000 | 10:11:35.056 | 10:24:44.865 | yes |
| EstimatedState | 15800 | 20.000 | 10:11:35.025 | 10:24:44.975 | yes |
| NavigationUncertainty | 15800 | 20.000 | 10:11:35.025 | 10:24:44.975 | yes |
| NavigationData | 15800 | 20.000 | 10:11:35.025 | 10:24:44.975 | yes |
| AllocatedControlTorques | 15698 | 19.871 | 10:11:39.981 | 10:24:44.975 |  |
| DesiredPitch | 15697 | 19.870 | 10:11:40.175 | 10:24:44.975 |  |
| DesiredHeadingRate | 15697 | 19.870 | 10:11:40.175 | 10:24:44.975 |  |
| DesiredControl | 15697 | 19.870 | 10:11:40.175 | 10:24:44.975 |  |
| FuelLevel | 13986 | 17.704 | 10:11:35.248 | 10:24:44.840 |  |
| PowerChannelState | 11625 | 14.715 | 10:11:35.582 | 10:24:44.240 |  |
| DevDataBinary | 9480 | 12.000 | 10:11:35.026 | 10:24:44.867 |  |
| DevDataText | 8365 | 10.589 | 10:11:35.024 | 10:24:44.835 |  |
| Rpm | 7900 | 10.000 | 10:11:34.985 | 10:24:44.884 | yes |
| Pressure | 7881 | 9.976 | 10:11:35.037 | 10:24:44.865 | yes |
| Depth | 7881 | 9.976 | 10:11:35.037 | 10:24:44.865 | yes |
| SoundSpeed | 7881 | 9.976 | 10:11:35.038 | 10:24:44.865 | yes |
| SetThrusterActuation | 7850 | 9.937 | 10:11:39.981 | 10:24:44.884 | yes |
| DesiredHeading | 6068 | 7.681 | 10:11:40.125 | 10:24:44.925 | yes |
| Conductivity | 3950 | 5.000 | 10:11:35.037 | 10:24:44.835 | yes |
| WaterDensity | 3950 | 5.000 | 10:11:35.037 | 10:24:44.835 | yes |
| Salinity | 3950 | 5.000 | 10:11:35.037 | 10:24:44.835 | yes |
| GroundVelocity | 3950 | 5.000 | 10:11:35.056 | 10:24:44.865 | yes |
| WaterVelocity | 3950 | 5.000 | 10:11:35.058 | 10:24:44.867 | yes |
| SatellitesInView | 3160 | 4.000 | 10:11:35.312 | 10:24:44.240 | yes |
| PlanControlState | 2265 | 2.867 | 10:11:35.224 | 10:24:44.825 | yes |
| VehicleState | 2204 | 2.790 | 10:11:35.481 | 10:24:44.981 | yes |
| TransportBindings | 1162 | 1.471 | 10:11:35.026 | 10:11:35.026 |  |
| Heartbeat | 1081 | 1.368 | 10:11:34.007 | 10:24:44.693 |  |
| ManeuverControlState | 854 | 1.081 | 10:11:35.481 | 10:24:44.925 | yes |
| GpsFix | 791 | 1.001 | 09:35:27.325 | 10:24:44.240 | yes |
| Pulse | 790 | 1.000 | 10:11:35.026 | 10:24:44.031 |  |
| VehicleMedium | 790 | 1.000 | 10:11:35.974 | 10:24:44.973 | yes |
| StorageUsage | 775 | 0.981 | 10:11:35.581 | 10:24:44.240 |  |
| EntityMonitoringState | 775 | 0.981 | 10:11:35.581 | 10:24:44.240 |  |
| AlignmentState | 775 | 0.981 | 10:11:35.625 | 10:24:44.275 | yes |
| PathControlState | 744 | 0.942 | 10:11:39.981 | 10:24:44.925 | yes |
| RSSI | 269 | 0.341 | 10:11:38.608 | 10:24:44.243 |  |
| Announce | 238 | 0.301 | 10:11:37.155 | 10:24:43.508 | yes |
| LogBookEntry | 233 | 0.295 | 10:11:35.481 | 10:24:44.981 | yes |
| EntityInfo | 155 | 0.196 | 10:11:35.000 | 10:24:44.982 | yes |
| QueryEntityInfo | 110 | 0.139 | 10:11:34.982 | 10:11:34.982 |  |
| EntityActivationState | 95 | 0.120 | 10:11:35.481 | 10:24:44.982 | yes |
| ReportControl | 56 | 0.071 | 10:12:10.525 | 10:24:10.875 |  |
| UamTxStatus | 56 | 0.071 | 10:12:10.545 | 10:24:11.443 | yes |
| EntityList | 38 | 0.048 | 10:11:54.011 | 10:24:42.233 | yes |
| UamTxFrame | 28 | 0.035 | 10:12:10.525 | 10:24:10.875 | yes |
| GnssHwMon | 26 | 0.033 | 10:11:52.315 | 10:24:29.313 | yes |
| SetEntityParameters | 24 | 0.030 | 10:11:35.575 | 10:23:43.175 |  |
| VehicleCommand | 19 | 0.024 | 10:11:34.983 | 10:24:44.981 |  |
| AcousticLink | 17 | 0.022 | 10:13:59.131 | 10:23:57.346 |  |
| UamRxFrame | 17 | 0.022 | 10:13:59.131 | 10:23:57.346 | yes |
| RemoteActionsRequest | 16 | 0.020 | 10:11:54.011 | 10:24:40.070 |  |
| TextMessage | 15 | 0.019 | 10:13:59.131 | 10:23:57.346 | yes |
| PlanDB | 14 | 0.018 | 10:11:54.011 | 10:24:39.911 |  |
| LblConfig | 14 | 0.018 | 10:11:54.011 | 10:24:39.927 |  |
| VersionInfo | 9 | 0.011 | 10:11:35.000 | 10:11:35.057 |  |
| Goto | 8 | 0.010 | 10:11:39.981 | 10:23:31.481 |  |
| DesiredPath | 8 | 0.010 | 10:11:39.981 | 10:23:31.481 | yes |
| DesiredZ | 8 | 0.010 | 10:11:39.981 | 10:23:31.481 | yes |
| DesiredSpeed | 8 | 0.010 | 10:11:39.981 | 10:23:31.481 | yes |
| ControlLoops | 6 | 0.008 | 10:11:39.981 | 10:11:39.981 |  |
| LoggingControl | 3 | 0.004 | 10:11:34.982 | 10:24:44.983 | yes |
| PushEntityParameters | 3 | 0.004 | 10:11:34.982 | 10:11:34.983 |  |
| PopEntityParameters | 3 | 0.004 | 10:24:44.981 | 10:24:44.982 |  |
| PlanSpecification | 1 | 0.001 | 10:11:34.983 | 10:11:34.983 |  |
| OperationalLimits | 1 | 0.001 | 09:46:52.474 | 09:46:52.474 |  |
| IdleManeuver | 1 | 0.001 | 10:11:35.481 | 10:11:35.481 |  |
| StopManeuver | 1 | 0.001 | 10:11:39.481 | 10:11:39.481 |  |
| PlanControl | 1 | 0.001 | 10:24:44.981 | 10:24:44.981 | yes |
| PlanStatistics | 1 | 0.001 | 10:24:44.982 | 10:24:44.982 |  |

## Source entities per decoded message type

| message | entity id | label | count |
|---|---|---|---|
| Acceleration | 78 | AHRS | 39499 |
| AlignmentState | 49 | Navigation | 775 |
| AngularVelocity | 78 | AHRS | 39499 |
| Announce | 96 | Service Announcer | 158 |
| Announce | 1 | Motor Controller | 76 |
| Announce | 23 | Compass Calibration Maneuver | 4 |
| Conductivity | 70 | CTD | 3950 |
| Depth | 70 | CTD | 3950 |
| Depth | 79 | DVL | 3931 |
| DesiredHeading | 21 | Path Control | 6068 |
| DesiredPath | 28 | Goto Maneuver | 8 |
| DesiredSpeed | 21 | Path Control | 8 |
| DesiredZ | 22 | Path Control - Bottom Track | 8 |
| Distance | 80 | DVL - Beam 0 | 3950 |
| Distance | 81 | DVL - Beam 1 | 3950 |
| Distance | 82 | DVL - Beam 2 | 3950 |
| Distance | 83 | DVL - Beam 3 | 3950 |
| Distance | 84 | DVL Filtered | 3950 |
| EntityActivationState | 26 | Multiplexer Maneuver | 54 |
| EntityActivationState | 76 | Multibeam | 9 |
| EntityActivationState | 50 | LBL Ranger | 9 |
| EntityActivationState | 69 | Sidescan | 8 |
| EntityActivationState | 21 | Path Control | 3 |
| EntityActivationState | 12 | Attitude | 3 |
| EntityActivationState | 11 | Allocator | 3 |
| EntityActivationState | 20 | Speed Control | 3 |
| EntityActivationState | 18 | Diving | 3 |
| EntityInfo | 50 | LBL Ranger | 10 |
| EntityInfo | 76 | Multibeam | 10 |
| EntityInfo | 69 | Sidescan | 9 |
| EntityInfo | 85 | IO Bridge | 2 |
| EntityInfo | 86 | Clock | 2 |
| EntityInfo | 87 | Synthetic Clock | 2 |
| EntityInfo | 70 | CTD | 2 |
| EntityInfo | 79 | DVL | 2 |
| EntityInfo | 80 | DVL - Beam 0 | 2 |
| EntityInfo | 81 | DVL - Beam 1 | 2 |
| EntityInfo | 82 | DVL - Beam 2 | 2 |
| EntityInfo | 83 | DVL - Beam 3 | 2 |
| EntityInfo | 84 | DVL Filtered | 2 |
| EntityInfo | 109 | LEDs | 2 |
| EntityInfo | 71 | GPS | 2 |
| EntityInfo | 72 | GPS - Constellation GPS | 2 |
| EntityInfo | 73 | GPS - Constellation GLONASS | 2 |
| EntityInfo | 74 | GPS - Constellation BEIDOU | 2 |
| EntityInfo | 75 | GPS - Constellation GALILEO | 2 |
| EntityInfo | 96 | Service Announcer | 2 |
| EntityInfo | 101 | HTTP Server | 2 |
| EntityInfo | 92 | Safety Supervisor | 2 |
| EntityInfo | 0 | Daemon | 1 |
| EntityInfo | 10 | Text Message Parser | 1 |
| EntityInfo | 11 | Allocator | 1 |
| EntityInfo | 12 | Attitude | 1 |
| EntityInfo | 13 | Roll Parcel | 1 |
| EntityInfo | 14 | Pitch Parcel | 1 |
| EntityInfo | 15 | Depth Parcel | 1 |
| EntityInfo | 16 | Heading Parcel | 1 |
| EntityInfo | 17 | Heading Rate Parcel | 1 |
| EntityInfo | 20 | Speed Control | 1 |
| EntityInfo | 21 | Path Control | 1 |
| EntityInfo | 22 | Path Control - Bottom Track | 1 |
| EntityInfo | 23 | Compass Calibration Maneuver | 1 |
| EntityInfo | 24 | Endurance Test Maneuver | 1 |
| EntityInfo | 25 | Follow Reference Maneuver | 1 |
| EntityInfo | 26 | Multiplexer Maneuver | 1 |
| EntityInfo | 27 | Idle Maneuver | 1 |
| EntityInfo | 28 | Goto Maneuver | 1 |
| EntityInfo | 29 | Launch Maneuver | 1 |
| EntityInfo | 30 | Loiter Maneuver | 1 |
| EntityInfo | 31 | Station Keeping Maneuver | 1 |
| EntityInfo | 32 | YoYo Maneuver | 1 |
| EntityInfo | 33 | Rows Maneuver | 1 |
| EntityInfo | 34 | Follow Path Maneuver | 1 |
| EntityInfo | 35 | Elevator Maneuver | 1 |
| EntityInfo | 36 | Pop Up Maneuver | 1 |
| EntityInfo | 37 | Dislodge Maneuver | 1 |
| EntityInfo | 38 | Alignment Maneuver | 1 |
| EntityInfo | 39 | Magnetometer Maneuver | 1 |
| EntityInfo | 40 | Teleoperation Maneuver | 1 |
| EntityInfo | 41 | Collisions | 1 |
| EntityInfo | 42 | Entity Monitor | 1 |
| EntityInfo | 43 | Health Monitor | 1 |
| EntityInfo | 47 | Servo Monitor | 1 |
| EntityInfo | 48 | Tachograph | 1 |
| EntityInfo | 51 | Plan Engine | 1 |
| EntityInfo | 52 | Plan Generator | 1 |
| EntityInfo | 53 | Power Supply | 1 |
| EntityInfo | 54 | Battery Pack 0 | 1 |
| EntityInfo | 55 | Battery Pack 1 | 1 |
| EntityInfo | 56 | Battery Pack 2 | 1 |
| EntityInfo | 57 | Battery Pack 3 | 1 |
| EntityInfo | 58 | Battery Pack 4 | 1 |
| EntityInfo | 59 | Battery Pack 5 | 1 |
| EntityInfo | 60 | Battery Pack 6 | 1 |
| EntityInfo | 61 | Battery Pack 7 | 1 |
| EntityInfo | 62 | Batteries | 1 |
| EntityInfo | 63 | Power Supply (Payload) | 1 |
| EntityInfo | 64 | Power Supply (+12VDC) | 1 |
| EntityInfo | 65 | Power Supply (+5VDC) | 1 |
| EntityInfo | 66 | Power Supply (Tail) | 1 |
| EntityInfo | 67 | Medium Sensor | 1 |
| EntityInfo | 68 | Leak Sensor | 1 |
| EntityInfo | 77 | Echo Sounder | 1 |
| EntityInfo | 89 | Power Supervisor | 1 |
| EntityInfo | 91 | Report Supervisor | 1 |
| EntityInfo | 78 | AHRS | 1 |
| EntityInfo | 94 | Zerotier Service | 1 |
| EntityInfo | 97 | Cache | 1 |
| EntityInfo | 99 | Acoustic Modem | 1 |
| EntityInfo | 100 | GSM | 1 |
| EntityInfo | 102 | Iridium Modem | 1 |
| EntityInfo | 103 | Log Book | 1 |
| EntityInfo | 49 | Navigation | 1 |
| EntityInfo | 105 | Mobile Internet | 1 |
| EntityInfo | 107 | Acoustic Access Controller | 1 |
| EntityInfo | 108 | UDP | 1 |
| EntityInfo | 106 | TCP Server (Settings) | 1 |
| EntityInfo | 104 | Logger | 1 |
| EntityInfo | 1 | Motor Controller | 1 |
| EntityInfo | 2 | Motor | 1 |
| EntityInfo | 3 | Motor Controller (Bridge) | 1 |
| EntityInfo | 4 | Motor Controller (MCU) | 1 |
| EntityInfo | 5 | Servo Controller | 1 |
| EntityInfo | 6 | Servo Controller - Servo 0 | 1 |
| EntityInfo | 7 | Servo Controller - Servo 1 | 1 |
| EntityInfo | 8 | Servo Controller - Servo 2 | 1 |
| EntityInfo | 9 | Servo Controller - Servo 3 | 1 |
| EntityInfo | 19 | Remote Control | 1 |
| EntityInfo | 18 | Diving | 1 |
| EntityInfo | 46 | Operational Limits | 1 |
| EntityInfo | 88 | GPIO Supervisor | 1 |
| EntityInfo | 95 | Vehicle Supervisor | 1 |
| EntityInfo | 98 | Service Discovery | 1 |
| EntityInfo | 44 | Medium | 1 |
| EntityInfo | 45 | Navigation Monitor | 1 |
| EntityInfo | 90 | Recovery Supervisor | 1 |
| EntityInfo | 93 | Storage Supervisor | 1 |
| EntityList | 0 | Daemon | 24 |
| EntityList | 1 | Motor Controller | 14 |
| EstimatedState | 49 | Navigation | 15800 |
| EulerAngles | 78 | AHRS | 39499 |
| GnssHwMon | 71 | GPS | 26 |
| GpsFix | 71 | GPS | 790 |
| GpsFix | 49 | Navigation | 1 |
| GroundVelocity | 79 | DVL | 3950 |
| LogBookEntry | 107 | Acoustic Access Controller | 170 |
| LogBookEntry | 10 | Text Message Parser | 30 |
| LogBookEntry | 108 | UDP | 10 |
| LogBookEntry | 51 | Plan Engine | 9 |
| LogBookEntry | 21 | Path Control | 8 |
| LogBookEntry | 95 | Vehicle Supervisor | 2 |
| LogBookEntry | 47 | Servo Monitor | 2 |
| LogBookEntry | 98 | Service Discovery | 1 |
| LogBookEntry | 102 | Iridium Modem | 1 |
| LoggingControl | 104 | Logger | 2 |
| LoggingControl | 51 | Plan Engine | 1 |
| MagneticField | 78 | AHRS | 39499 |
| ManeuverControlState | 28 | Goto Maneuver | 736 |
| ManeuverControlState | 27 | Idle Maneuver | 100 |
| ManeuverControlState | 26 | Multiplexer Maneuver | 18 |
| NavigationData | 49 | Navigation | 15800 |
| NavigationUncertainty | 49 | Navigation | 15800 |
| PathControlState | 21 | Path Control | 744 |
| PlanControl | 51 | Plan Engine | 1 |
| PlanControlState | 51 | Plan Engine | 2265 |
| Pressure | 70 | CTD | 3950 |
| Pressure | 79 | DVL | 3931 |
| Rpm | 2 | Motor | 7900 |
| Salinity | 70 | CTD | 3950 |
| SatellitesInView | 74 | GPS - Constellation BEIDOU | 790 |
| SatellitesInView | 75 | GPS - Constellation GALILEO | 790 |
| SatellitesInView | 73 | GPS - Constellation GLONASS | 790 |
| SatellitesInView | 72 | GPS - Constellation GPS | 790 |
| SetThrusterActuation | 20 | Speed Control | 7850 |
| SoundSpeed | 70 | CTD | 3950 |
| SoundSpeed | 79 | DVL | 3931 |
| Temperature | 53 | Power Supply | 3996 |
| Temperature | 70 | CTD | 3950 |
| Temperature | 79 | DVL | 3931 |
| Temperature | 54 | Battery Pack 0 | 1998 |
| Temperature | 55 | Battery Pack 1 | 1998 |
| Temperature | 56 | Battery Pack 2 | 1998 |
| Temperature | 57 | Battery Pack 3 | 1998 |
| Temperature | 58 | Battery Pack 4 | 1998 |
| Temperature | 59 | Battery Pack 5 | 1998 |
| Temperature | 4 | Motor Controller (MCU) | 384 |
| Temperature | 3 | Motor Controller (Bridge) | 384 |
| Temperature | 2 | Motor | 384 |
| TextMessage | 107 | Acoustic Access Controller | 15 |
| UamRxFrame | 99 | Acoustic Modem | 17 |
| UamTxFrame | 107 | Acoustic Access Controller | 28 |
| UamTxStatus | 99 | Acoustic Modem | 56 |
| VehicleMedium | 44 | Medium | 790 |
| VehicleState | 95 | Vehicle Supervisor | 2204 |
| WaterDensity | 70 | CTD | 3950 |
| WaterVelocity | 79 | DVL | 3950 |

## Entity table (EntityInfo)

0=Daemon, 1=Motor Controller, 2=Motor, 3=Motor Controller (Bridge), 4=Motor Controller (MCU), 5=Servo Controller, 6=Servo Controller - Servo 0, 7=Servo Controller - Servo 1, 8=Servo Controller - Servo 2, 9=Servo Controller - Servo 3, 10=Text Message Parser, 11=Allocator, 12=Attitude, 13=Roll Parcel, 14=Pitch Parcel, 15=Depth Parcel, 16=Heading Parcel, 17=Heading Rate Parcel, 18=Diving, 19=Remote Control, 20=Speed Control, 21=Path Control, 22=Path Control - Bottom Track, 23=Compass Calibration Maneuver, 24=Endurance Test Maneuver, 25=Follow Reference Maneuver, 26=Multiplexer Maneuver, 27=Idle Maneuver, 28=Goto Maneuver, 29=Launch Maneuver, 30=Loiter Maneuver, 31=Station Keeping Maneuver, 32=YoYo Maneuver, 33=Rows Maneuver, 34=Follow Path Maneuver, 35=Elevator Maneuver, 36=Pop Up Maneuver, 37=Dislodge Maneuver, 38=Alignment Maneuver, 39=Magnetometer Maneuver, 40=Teleoperation Maneuver, 41=Collisions, 42=Entity Monitor, 43=Health Monitor, 44=Medium, 45=Navigation Monitor, 46=Operational Limits, 47=Servo Monitor, 48=Tachograph, 49=Navigation, 50=LBL Ranger, 51=Plan Engine, 52=Plan Generator, 53=Power Supply, 54=Battery Pack 0, 55=Battery Pack 1, 56=Battery Pack 2, 57=Battery Pack 3, 58=Battery Pack 4, 59=Battery Pack 5, 60=Battery Pack 6, 61=Battery Pack 7, 62=Batteries, 63=Power Supply (Payload), 64=Power Supply (+12VDC), 65=Power Supply (+5VDC), 66=Power Supply (Tail), 67=Medium Sensor, 68=Leak Sensor, 69=Sidescan, 70=CTD, 71=GPS, 72=GPS - Constellation GPS, 73=GPS - Constellation GLONASS, 74=GPS - Constellation BEIDOU, 75=GPS - Constellation GALILEO, 76=Multibeam, 77=Echo Sounder, 78=AHRS, 79=DVL, 80=DVL - Beam 0, 81=DVL - Beam 1, 82=DVL - Beam 2, 83=DVL - Beam 3, 84=DVL Filtered, 85=IO Bridge, 86=Clock, 87=Synthetic Clock, 88=GPIO Supervisor, 89=Power Supervisor, 90=Recovery Supervisor, 91=Report Supervisor, 92=Safety Supervisor, 93=Storage Supervisor, 94=Zerotier Service, 95=Vehicle Supervisor, 96=Service Announcer, 97=Cache, 98=Service Discovery, 99=Acoustic Modem, 100=GSM, 101=HTTP Server, 102=Iridium Modem, 103=Log Book, 104=Logger, 105=Mobile Internet, 106=TCP Server (Settings), 107=Acoustic Access Controller, 108=UDP, 109=LEDs

## Requested messages NOT present in this log

AcousticOperation, Chlorophyll, DvlRejection, EstimatedStreamVelocity, GpsFixRejection, LblEstimate, LblRangeAcceptance, SimulatedState, Turbidity, UamRxRange, UamTxRange, UsblAngles, UsblAnglesExtended, UsblConfig, UsblFix, UsblFixExtended, UsblModem, UsblPosition, UsblPositionExtended, VelocityDelta
