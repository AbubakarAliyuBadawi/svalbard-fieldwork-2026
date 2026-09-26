# Inventory: 074948_08_09_sidescan

Source: `074948_08_09_sidescan/Data.lsf.gz` (51.5 MB gz), IMC 5.5.4.9, sync 0xFE55, byte order little-endian.

Messages: 2187963. CRC-16 checked on 9330 sampled messages, 0 failures.

## Vehicle identity

- Config.ini `Vehicle =` : **lauv-marie**
- Announce sys_name (own system, src 8259): **['lauv-marie']**
- LoggingControl label: `20260908/074948_08_09_sidescan`
- IMC source addresses seen: {8259: 2187851, 23839: 39, 18467: 37, 18474: 29, 32932: 7} (8259 = the vehicle itself)

## Time span (header timestamps, vehicle clock)

- start: 1788853788.380 = 2026-09-08 07:49:48.379Z
- end:   1788855880.879 = 2026-09-08 08:24:40.878Z
- duration: 2092.5 s = 34.87 min

## Clock check: header timestamp minus GPS UTC time of fix (s)

| entity | n | median | mean | std | min | max |
|---|---|---|---|---|---|---|
| GPS | 2092 | +0.243 | +0.247 | 0.036 | +0.085 | +0.441 |
| Navigation | 1 | +0.316 | +0.316 | nan | +0.316 | +0.316 |

## Message types (count, mean rate over the log, first/last time)

| message | count | rate [Hz] | first | last | decoded |
|---|---|---|---|---|---|
| ControlParcel | 236753 | 113.144 | 07:49:48.416 | 08:24:40.865 |  |
| SetServoPosition | 166280 | 79.465 | 07:49:48.416 | 08:24:40.865 |  |
| Current | 163636 | 78.201 | 07:49:48.430 | 08:24:40.830 |  |
| EntityState | 129492 | 61.884 | 07:49:48.402 | 08:24:40.877 |  |
| CpuUsage | 117990 | 56.387 | 07:49:49.016 | 08:24:40.112 |  |
| EulerAngles | 104640 | 50.007 | 07:49:48.381 | 08:24:40.863 | yes |
| Acceleration | 104640 | 50.007 | 07:49:48.381 | 08:24:40.863 | yes |
| AngularVelocity | 104640 | 50.007 | 07:49:48.381 | 08:24:40.863 | yes |
| MagneticField | 104640 | 50.007 | 07:49:48.381 | 08:24:40.863 | yes |
| ServoPosition | 83692 | 39.996 | 07:49:48.439 | 08:24:40.820 |  |
| Voltage | 80961 | 38.691 | 07:49:48.430 | 08:24:40.830 |  |
| Temperature | 64807 | 30.971 | 07:49:48.471 | 08:24:40.749 | yes |
| Distance | 55505 | 26.526 | 07:49:48.471 | 08:24:40.708 | yes |
| EstimatedState | 41850 | 20.000 | 07:49:48.416 | 08:24:40.865 | yes |
| NavigationUncertainty | 41850 | 20.000 | 07:49:48.416 | 08:24:40.865 | yes |
| NavigationData | 41850 | 20.000 | 07:49:48.416 | 08:24:40.865 | yes |
| AllocatedControlTorques | 41568 | 19.865 | 07:49:48.416 | 08:24:40.865 |  |
| DesiredControl | 41564 | 19.863 | 07:49:48.416 | 08:24:40.865 |  |
| DesiredHeadingRate | 41559 | 19.861 | 07:49:48.461 | 08:24:40.865 |  |
| DesiredPitch | 41559 | 19.861 | 07:49:48.461 | 08:24:40.865 |  |
| SonarData | 37758 | 18.044 | 07:50:25.961 | 08:24:40.709 |  |
| FuelLevel | 36946 | 17.656 | 07:49:48.686 | 08:24:40.678 |  |
| DevDataBinary | 36106 | 17.255 | 07:49:48.471 | 08:24:40.734 |  |
| PowerChannelState | 31050 | 14.839 | 07:49:49.022 | 08:24:40.114 |  |
| Rpm | 20925 | 10.000 | 07:49:48.430 | 08:24:40.830 | yes |
| SetThrusterActuation | 20787 | 9.934 | 07:49:48.430 | 08:24:40.830 | yes |
| DevDataText | 20188 | 9.648 | 07:49:48.417 | 08:24:40.749 |  |
| Pressure | 19532 | 9.334 | 07:49:48.471 | 08:24:40.749 | yes |
| SoundSpeed | 19532 | 9.334 | 07:49:48.471 | 08:24:40.749 | yes |
| Depth | 19532 | 9.334 | 07:49:48.471 | 08:24:40.749 | yes |
| DesiredHeading | 15999 | 7.646 | 07:49:53.516 | 08:24:40.766 | yes |
| Conductivity | 10464 | 5.001 | 07:49:48.474 | 08:24:40.749 | yes |
| WaterDensity | 10464 | 5.001 | 07:49:48.474 | 08:24:40.749 | yes |
| Salinity | 10464 | 5.001 | 07:49:48.475 | 08:24:40.749 | yes |
| GroundVelocity | 9068 | 4.334 | 07:49:48.471 | 08:24:40.708 | yes |
| WaterVelocity | 9068 | 4.334 | 07:49:48.473 | 08:24:40.709 | yes |
| SatellitesInView | 8368 | 3.999 | 07:49:49.308 | 08:24:40.113 | yes |
| ManeuverControlState | 7233 | 3.457 | 07:49:48.877 | 08:24:40.416 | yes |
| VehicleState | 6732 | 3.217 | 07:49:48.878 | 08:24:40.877 | yes |
| PlanControlState | 6000 | 2.867 | 07:49:48.666 | 08:24:40.865 | yes |
| Heartbeat | 2160 | 1.032 | 07:49:48.543 | 08:24:40.112 |  |
| GpsFix | 2093 | 1.000 | 07:13:27.315 | 08:24:40.113 | yes |
| VehicleMedium | 2093 | 1.000 | 07:49:48.864 | 08:24:40.864 | yes |
| Pulse | 2093 | 1.000 | 07:49:49.020 | 08:24:40.734 |  |
| StorageUsage | 2070 | 0.989 | 07:49:49.021 | 08:24:40.112 |  |
| EntityMonitoringState | 2070 | 0.989 | 07:49:49.022 | 08:24:40.112 |  |
| AlignmentState | 2070 | 0.989 | 07:49:49.065 | 08:24:40.115 | yes |
| GpsFixRejection | 2056 | 0.983 | 07:50:21.286 | 08:24:36.391 | yes |
| PathControlState | 1968 | 0.941 | 07:49:53.416 | 08:24:40.416 | yes |
| TransportBindings | 1162 | 0.555 | 07:49:48.418 | 07:49:48.419 |  |
| RSSI | 622 | 0.297 | 07:49:50.034 | 08:24:37.885 |  |
| Announce | 433 | 0.207 | 07:49:48.112 | 08:24:39.510 | yes |
| EntityActivationState | 272 | 0.130 | 07:49:48.877 | 08:24:40.878 | yes |
| LogBookEntry | 267 | 0.128 | 07:49:48.877 | 08:24:40.877 | yes |
| EntityInfo | 185 | 0.088 | 07:49:48.391 | 08:24:40.878 | yes |
| QueryEntityInfo | 110 | 0.053 | 07:49:48.379 | 07:49:48.379 |  |
| ReportControl | 80 | 0.038 | 07:50:01.566 | 08:24:37.877 |  |
| UamTxStatus | 78 | 0.037 | 07:50:01.583 | 08:24:38.458 | yes |
| GnssHwMon | 69 | 0.033 | 07:49:59.690 | 08:24:17.697 | yes |
| SetEntityParameters | 63 | 0.030 | 07:49:49.016 | 08:21:34.378 |  |
| VehicleCommand | 45 | 0.022 | 07:49:48.380 | 08:24:40.877 |  |
| UamTxFrame | 39 | 0.019 | 07:50:01.566 | 08:24:37.877 | yes |
| DesiredSpeed | 28 | 0.013 | 07:49:48.461 | 08:24:38.316 | yes |
| DesiredPath | 23 | 0.011 | 07:49:53.416 | 08:24:38.315 | yes |
| DesiredZ | 23 | 0.011 | 07:49:53.416 | 08:24:38.316 | yes |
| Goto | 19 | 0.009 | 07:51:05.377 | 08:18:54.377 |  |
| ControlLoops | 18 | 0.009 | 07:49:48.877 | 08:24:38.316 |  |
| VersionInfo | 8 | 0.004 | 07:49:48.392 | 07:49:48.478 |  |
| AcousticLink | 6 | 0.003 | 07:51:28.346 | 07:55:48.218 |  |
| UamRxFrame | 6 | 0.003 | 07:51:28.346 | 07:55:48.218 | yes |
| LoggingControl | 5 | 0.002 | 07:49:48.379 | 08:24:40.878 | yes |
| EntityList | 4 | 0.002 | 07:50:01.544 | 07:50:02.736 | yes |
| RemoteActionsRequest | 4 | 0.002 | 07:50:01.544 | 07:50:02.761 |  |
| PushEntityParameters | 3 | 0.001 | 07:49:48.379 | 07:49:48.380 |  |
| TextMessage | 3 | 0.001 | 07:51:28.346 | 07:55:48.218 | yes |
| PowerChannelControl | 3 | 0.001 | 07:52:31.066 | 07:52:39.070 |  |
| PopEntityParameters | 3 | 0.001 | 08:24:40.878 | 08:24:40.878 |  |
| PlanDB | 2 | 0.001 | 07:50:01.544 | 07:50:01.444 |  |
| LblConfig | 2 | 0.001 | 07:50:01.544 | 07:50:01.443 |  |
| PlanSpecification | 1 | 0.000 | 07:49:48.380 | 07:49:48.380 |  |
| OperationalLimits | 1 | 0.000 | 07:37:19.365 | 07:37:19.365 |  |
| IdleManeuver | 1 | 0.000 | 07:49:48.877 | 07:49:48.877 |  |
| StopManeuver | 1 | 0.000 | 07:49:52.877 | 07:49:52.877 |  |
| Elevator | 1 | 0.000 | 07:49:53.377 | 07:49:53.377 |  |
| PulseDetectionControl | 1 | 0.000 | 07:52:39.194 | 07:52:39.194 |  |
| PopUp | 1 | 0.000 | 08:21:34.377 | 08:21:34.377 |  |
| IridiumMsgTx | 1 | 0.000 | 08:24:37.877 | 08:24:37.877 |  |
| SmsRequest | 1 | 0.000 | 08:24:37.877 | 08:24:37.877 |  |
| IridiumTxStatus | 1 | 0.000 | 08:24:37.877 | 08:24:37.877 |  |
| SmsStatus | 1 | 0.000 | 08:24:37.877 | 08:24:37.877 |  |
| PlanControl | 1 | 0.000 | 08:24:40.877 | 08:24:40.877 | yes |
| PlanStatistics | 1 | 0.000 | 08:24:40.878 | 08:24:40.878 |  |

## Source entities per decoded message type

| message | entity id | label | count |
|---|---|---|---|
| Acceleration | 78 | AHRS | 104640 |
| AlignmentState | 49 | Navigation | 2070 |
| AngularVelocity | 78 | AHRS | 104640 |
| Announce | 96 | Service Announcer | 420 |
| Announce | 1 | Motor Controller | 9 |
| Announce | 23 | Compass Calibration Maneuver | 4 |
| Conductivity | 70 | CTD | 10464 |
| Depth | 70 | CTD | 10464 |
| Depth | 79 | DVL | 9068 |
| DesiredHeading | 21 | Path Control | 15999 |
| DesiredPath | 28 | Goto Maneuver | 19 |
| DesiredPath | 35 | Elevator Maneuver | 2 |
| DesiredPath | 36 | Pop Up Maneuver | 2 |
| DesiredSpeed | 21 | Path Control | 23 |
| DesiredSpeed | 19 | Remote Control | 5 |
| DesiredZ | 22 | Path Control - Bottom Track | 23 |
| Distance | 77 | Echo Sounder | 10165 |
| Distance | 80 | DVL - Beam 0 | 9068 |
| Distance | 81 | DVL - Beam 1 | 9068 |
| Distance | 82 | DVL - Beam 2 | 9068 |
| Distance | 83 | DVL - Beam 3 | 9068 |
| Distance | 84 | DVL Filtered | 9068 |
| EntityActivationState | 26 | Multiplexer Maneuver | 132 |
| EntityActivationState | 18 | Diving | 24 |
| EntityActivationState | 69 | Sidescan | 23 |
| EntityActivationState | 76 | Multibeam | 23 |
| EntityActivationState | 50 | LBL Ranger | 22 |
| EntityActivationState | 11 | Allocator | 12 |
| EntityActivationState | 12 | Attitude | 12 |
| EntityActivationState | 20 | Speed Control | 12 |
| EntityActivationState | 21 | Path Control | 9 |
| EntityActivationState | 19 | Remote Control | 3 |
| EntityInfo | 50 | LBL Ranger | 23 |
| EntityInfo | 69 | Sidescan | 22 |
| EntityInfo | 76 | Multibeam | 22 |
| EntityInfo | 98 | Service Discovery | 2 |
| EntityInfo | 101 | HTTP Server | 2 |
| EntityInfo | 44 | Medium | 2 |
| EntityInfo | 45 | Navigation Monitor | 2 |
| EntityInfo | 90 | Recovery Supervisor | 2 |
| EntityInfo | 93 | Storage Supervisor | 2 |
| EntityInfo | 85 | IO Bridge | 2 |
| EntityInfo | 86 | Clock | 2 |
| EntityInfo | 87 | Synthetic Clock | 2 |
| EntityInfo | 96 | Service Announcer | 2 |
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
| EntityInfo | 43 | Health Monitor | 1 |
| EntityInfo | 41 | Collisions | 1 |
| EntityInfo | 42 | Entity Monitor | 1 |
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
| EntityInfo | 94 | Zerotier Service | 1 |
| EntityInfo | 49 | Navigation | 1 |
| EntityInfo | 97 | Cache | 1 |
| EntityInfo | 99 | Acoustic Modem | 1 |
| EntityInfo | 100 | GSM | 1 |
| EntityInfo | 102 | Iridium Modem | 1 |
| EntityInfo | 105 | Mobile Internet | 1 |
| EntityInfo | 107 | Acoustic Access Controller | 1 |
| EntityInfo | 108 | UDP | 1 |
| EntityInfo | 103 | Log Book | 1 |
| EntityInfo | 104 | Logger | 1 |
| EntityInfo | 106 | TCP Server (Settings) | 1 |
| EntityInfo | 78 | AHRS | 1 |
| EntityInfo | 5 | Servo Controller | 1 |
| EntityInfo | 6 | Servo Controller - Servo 0 | 1 |
| EntityInfo | 7 | Servo Controller - Servo 1 | 1 |
| EntityInfo | 8 | Servo Controller - Servo 2 | 1 |
| EntityInfo | 9 | Servo Controller - Servo 3 | 1 |
| EntityInfo | 18 | Diving | 1 |
| EntityInfo | 19 | Remote Control | 1 |
| EntityInfo | 79 | DVL | 1 |
| EntityInfo | 80 | DVL - Beam 0 | 1 |
| EntityInfo | 81 | DVL - Beam 1 | 1 |
| EntityInfo | 82 | DVL - Beam 2 | 1 |
| EntityInfo | 83 | DVL - Beam 3 | 1 |
| EntityInfo | 84 | DVL Filtered | 1 |
| EntityInfo | 70 | CTD | 1 |
| EntityInfo | 1 | Motor Controller | 1 |
| EntityInfo | 2 | Motor | 1 |
| EntityInfo | 3 | Motor Controller (Bridge) | 1 |
| EntityInfo | 4 | Motor Controller (MCU) | 1 |
| EntityInfo | 46 | Operational Limits | 1 |
| EntityInfo | 109 | LEDs | 1 |
| EntityInfo | 88 | GPIO Supervisor | 1 |
| EntityInfo | 95 | Vehicle Supervisor | 1 |
| EntityInfo | 71 | GPS | 1 |
| EntityInfo | 72 | GPS - Constellation GPS | 1 |
| EntityInfo | 73 | GPS - Constellation GLONASS | 1 |
| EntityInfo | 74 | GPS - Constellation BEIDOU | 1 |
| EntityInfo | 75 | GPS - Constellation GALILEO | 1 |
| EntityList | 1 | Motor Controller | 2 |
| EntityList | 0 | Daemon | 2 |
| EstimatedState | 49 | Navigation | 41850 |
| EulerAngles | 78 | AHRS | 104640 |
| GnssHwMon | 71 | GPS | 69 |
| GpsFix | 71 | GPS | 2092 |
| GpsFix | 49 | Navigation | 1 |
| GpsFixRejection | 49 | Navigation | 2056 |
| GroundVelocity | 79 | DVL | 9068 |
| LogBookEntry | 107 | Acoustic Access Controller | 201 |
| LogBookEntry | 21 | Path Control | 26 |
| LogBookEntry | 51 | Plan Engine | 24 |
| LogBookEntry | 10 | Text Message Parser | 6 |
| LogBookEntry | 108 | UDP | 3 |
| LogBookEntry | 95 | Vehicle Supervisor | 2 |
| LogBookEntry | 76 | Multibeam | 1 |
| LogBookEntry | 47 | Servo Monitor | 1 |
| LogBookEntry | 49 | Navigation | 1 |
| LogBookEntry | 92 | Safety Supervisor | 1 |
| LogBookEntry | 100 | GSM | 1 |
| LoggingControl | 104 | Logger | 2 |
| LoggingControl | 76 | Multibeam | 1 |
| LoggingControl | 69 | Sidescan | 1 |
| LoggingControl | 51 | Plan Engine | 1 |
| MagneticField | 78 | AHRS | 104640 |
| ManeuverControlState | 36 | Pop Up Maneuver | 5308 |
| ManeuverControlState | 28 | Goto Maneuver | 1711 |
| ManeuverControlState | 27 | Idle Maneuver | 101 |
| ManeuverControlState | 35 | Elevator Maneuver | 69 |
| ManeuverControlState | 26 | Multiplexer Maneuver | 44 |
| NavigationData | 49 | Navigation | 41850 |
| NavigationUncertainty | 49 | Navigation | 41850 |
| PathControlState | 21 | Path Control | 1968 |
| PlanControl | 51 | Plan Engine | 1 |
| PlanControlState | 51 | Plan Engine | 6000 |
| Pressure | 70 | CTD | 10464 |
| Pressure | 79 | DVL | 9068 |
| Rpm | 2 | Motor | 20925 |
| Salinity | 70 | CTD | 10464 |
| SatellitesInView | 74 | GPS - Constellation BEIDOU | 2092 |
| SatellitesInView | 75 | GPS - Constellation GALILEO | 2092 |
| SatellitesInView | 73 | GPS - Constellation GLONASS | 2092 |
| SatellitesInView | 72 | GPS - Constellation GPS | 2092 |
| SetThrusterActuation | 20 | Speed Control | 20787 |
| SoundSpeed | 70 | CTD | 10464 |
| SoundSpeed | 79 | DVL | 9068 |
| Temperature | 53 | Power Supply | 10556 |
| Temperature | 70 | CTD | 10464 |
| Temperature | 79 | DVL | 9068 |
| Temperature | 54 | Battery Pack 0 | 5278 |
| Temperature | 55 | Battery Pack 1 | 5278 |
| Temperature | 56 | Battery Pack 2 | 5278 |
| Temperature | 57 | Battery Pack 3 | 5278 |
| Temperature | 58 | Battery Pack 4 | 5278 |
| Temperature | 59 | Battery Pack 5 | 5278 |
| Temperature | 4 | Motor Controller (MCU) | 1017 |
| Temperature | 3 | Motor Controller (Bridge) | 1017 |
| Temperature | 2 | Motor | 1017 |
| TextMessage | 107 | Acoustic Access Controller | 3 |
| UamRxFrame | 99 | Acoustic Modem | 6 |
| UamTxFrame | 107 | Acoustic Access Controller | 39 |
| UamTxStatus | 99 | Acoustic Modem | 78 |
| VehicleMedium | 44 | Medium | 2093 |
| VehicleState | 95 | Vehicle Supervisor | 6732 |
| WaterDensity | 70 | CTD | 10464 |
| WaterVelocity | 79 | DVL | 9068 |

## Entity table (EntityInfo)

0=Daemon, 1=Motor Controller, 2=Motor, 3=Motor Controller (Bridge), 4=Motor Controller (MCU), 5=Servo Controller, 6=Servo Controller - Servo 0, 7=Servo Controller - Servo 1, 8=Servo Controller - Servo 2, 9=Servo Controller - Servo 3, 10=Text Message Parser, 11=Allocator, 12=Attitude, 13=Roll Parcel, 14=Pitch Parcel, 15=Depth Parcel, 16=Heading Parcel, 17=Heading Rate Parcel, 18=Diving, 19=Remote Control, 20=Speed Control, 21=Path Control, 22=Path Control - Bottom Track, 23=Compass Calibration Maneuver, 24=Endurance Test Maneuver, 25=Follow Reference Maneuver, 26=Multiplexer Maneuver, 27=Idle Maneuver, 28=Goto Maneuver, 29=Launch Maneuver, 30=Loiter Maneuver, 31=Station Keeping Maneuver, 32=YoYo Maneuver, 33=Rows Maneuver, 34=Follow Path Maneuver, 35=Elevator Maneuver, 36=Pop Up Maneuver, 37=Dislodge Maneuver, 38=Alignment Maneuver, 39=Magnetometer Maneuver, 40=Teleoperation Maneuver, 41=Collisions, 42=Entity Monitor, 43=Health Monitor, 44=Medium, 45=Navigation Monitor, 46=Operational Limits, 47=Servo Monitor, 48=Tachograph, 49=Navigation, 50=LBL Ranger, 51=Plan Engine, 52=Plan Generator, 53=Power Supply, 54=Battery Pack 0, 55=Battery Pack 1, 56=Battery Pack 2, 57=Battery Pack 3, 58=Battery Pack 4, 59=Battery Pack 5, 60=Battery Pack 6, 61=Battery Pack 7, 62=Batteries, 63=Power Supply (Payload), 64=Power Supply (+12VDC), 65=Power Supply (+5VDC), 66=Power Supply (Tail), 67=Medium Sensor, 68=Leak Sensor, 69=Sidescan, 70=CTD, 71=GPS, 72=GPS - Constellation GPS, 73=GPS - Constellation GLONASS, 74=GPS - Constellation BEIDOU, 75=GPS - Constellation GALILEO, 76=Multibeam, 77=Echo Sounder, 78=AHRS, 79=DVL, 80=DVL - Beam 0, 81=DVL - Beam 1, 82=DVL - Beam 2, 83=DVL - Beam 3, 84=DVL Filtered, 85=IO Bridge, 86=Clock, 87=Synthetic Clock, 88=GPIO Supervisor, 89=Power Supervisor, 90=Recovery Supervisor, 91=Report Supervisor, 92=Safety Supervisor, 93=Storage Supervisor, 94=Zerotier Service, 95=Vehicle Supervisor, 96=Service Announcer, 97=Cache, 98=Service Discovery, 99=Acoustic Modem, 100=GSM, 101=HTTP Server, 102=Iridium Modem, 103=Log Book, 104=Logger, 105=Mobile Internet, 106=TCP Server (Settings), 107=Acoustic Access Controller, 108=UDP, 109=LEDs

## Requested messages NOT present in this log

AcousticOperation, Chlorophyll, DvlRejection, EstimatedStreamVelocity, LblEstimate, LblRangeAcceptance, SimulatedState, Turbidity, UamRxRange, UamTxRange, UsblAngles, UsblAnglesExtended, UsblConfig, UsblFix, UsblFixExtended, UsblModem, UsblPosition, UsblPositionExtended, VelocityDelta
