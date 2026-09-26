# Inventory: 094605_0700926LongYoYo1

Source: `094605_0700926LongYoYo1/Data.lsf.gz` (59.2 MB gz), IMC 5.4.23, sync 0xFE54, byte order little-endian.

Messages: 2966665. CRC-16 checked on 10889 sampled messages, 0 failures.

## Vehicle identity

- Config.ini `Vehicle =` : **lauv-thor**
- Announce sys_name (own system, src 8259): **['lauv-thor']**
- LoggingControl label: `20260907/094605_0700926LongYoYo1`
- IMC source addresses seen: {8217: 2966482, 18481: 171, 32880: 12} (8259 = the vehicle itself)

## Time span (header timestamps, vehicle clock)

- start: 1788774365.430 = 2026-09-07 09:46:05.430Z
- end:   1788777591.863 = 2026-09-07 10:39:51.863Z
- duration: 3226.4 s = 53.77 min

## Clock check: header timestamp minus GPS UTC time of fix (s)

| entity | n | median | mean | std | min | max |
|---|---|---|---|---|---|---|
| GPS | 3226 | -0.020 | -0.012 | 0.016 | -0.031 | +0.042 |
| Navigation | 1 | +0.174 | +0.174 | nan | +0.174 | +0.174 |

## Message types (count, mean rate over the log, first/last time)

| message | count | rate [Hz] | first | last | decoded |
|---|---|---|---|---|---|
| ControlParcel | 360979 | 111.882 | 09:46:05.453 | 10:39:51.824 |  |
| SetServoPosition | 255292 | 79.125 | 09:46:10.022 | 10:39:51.824 |  |
| Current | 217741 | 67.487 | 09:46:05.442 | 10:39:51.852 |  |
| EntityState | 202300 | 62.701 | 09:46:05.442 | 10:39:51.855 |  |
| CpuUsage | 177783 | 55.102 | 09:46:06.775 | 10:39:51.839 |  |
| EulerAngles | 161304 | 49.995 | 09:46:05.437 | 10:39:51.839 | yes |
| Acceleration | 161304 | 49.995 | 09:46:05.437 | 10:39:51.839 | yes |
| AngularVelocity | 161304 | 49.995 | 09:46:05.437 | 10:39:51.839 | yes |
| MagneticField | 161304 | 49.995 | 09:46:05.437 | 10:39:51.839 | yes |
| ServoPosition | 129032 | 39.992 | 09:46:05.453 | 10:39:51.784 |  |
| Voltage | 96729 | 29.980 | 09:46:05.442 | 10:39:51.852 |  |
| Distance | 80660 | 25.000 | 09:46:05.616 | 10:39:51.821 | yes |
| EstimatedState | 64528 | 20.000 | 09:46:05.474 | 10:39:51.824 | yes |
| NavigationUncertainty | 64528 | 20.000 | 09:46:05.474 | 10:39:51.824 | yes |
| NavigationData | 64528 | 20.000 | 09:46:05.474 | 10:39:51.824 | yes |
| AllocatedControlTorques | 63817 | 19.779 | 09:46:10.022 | 10:39:51.824 |  |
| DesiredHeadingRate | 63804 | 19.775 | 09:46:10.174 | 10:39:51.824 |  |
| DesiredControl | 63804 | 19.775 | 09:46:10.174 | 10:39:51.824 |  |
| Temperature | 51896 | 16.085 | 09:46:05.440 | 10:39:51.848 | yes |
| PowerChannelState | 37428 | 11.600 | 09:46:06.819 | 10:39:51.853 |  |
| Rpm | 32264 | 10.000 | 09:46:05.504 | 10:39:51.804 | yes |
| DevDataBinary | 32264 | 10.000 | 09:46:05.616 | 10:39:51.823 |  |
| SetThrusterActuation | 31925 | 9.895 | 09:46:10.022 | 10:39:51.804 | yes |
| DesiredHeading | 24904 | 7.719 | 09:46:10.124 | 10:39:51.774 | yes |
| Pressure | 19359 | 6.000 | 09:46:05.616 | 10:39:51.821 | yes |
| SoundSpeed | 19359 | 6.000 | 09:46:05.616 | 10:39:51.821 | yes |
| Depth | 19359 | 6.000 | 09:46:05.616 | 10:39:51.821 | yes |
| DesiredPitch | 18840 | 5.839 | 09:46:10.174 | 10:39:51.824 |  |
| DevDataText | 16545 | 5.128 | 09:46:05.977 | 10:39:51.852 |  |
| GroundVelocity | 16132 | 5.000 | 09:46:05.616 | 10:39:51.821 | yes |
| WaterVelocity | 16121 | 4.997 | 09:46:05.618 | 10:39:51.823 | yes |
| ManeuverControlState | 10082 | 3.125 | 09:46:05.434 | 10:39:51.854 | yes |
| VehicleState | 9252 | 2.868 | 09:46:05.516 | 10:39:51.516 | yes |
| PlanControlState | 9231 | 2.861 | 09:46:05.435 | 10:39:51.724 | yes |
| Heartbeat | 3255 | 1.009 | 09:46:06.885 | 10:39:51.839 |  |
| GpsFix | 3227 | 1.000 | 09:21:42.173 | 10:39:51.017 | yes |
| FuelLevel | 3227 | 1.000 | 09:46:05.465 | 10:39:51.465 |  |
| VehicleMedium | 3227 | 1.000 | 09:46:05.467 | 10:39:51.467 | yes |
| Conductivity | 3227 | 1.000 | 09:46:06.034 | 10:39:51.741 | yes |
| Salinity | 3227 | 1.000 | 09:46:06.034 | 10:39:51.741 | yes |
| WaterDensity | 3227 | 1.000 | 09:46:06.034 | 10:39:51.741 | yes |
| Chlorophyll | 3227 | 1.000 | 09:46:06.034 | 10:39:51.741 | yes |
| Turbidity | 3227 | 1.000 | 09:46:06.034 | 10:39:51.742 | yes |
| Pulse | 3226 | 1.000 | 09:46:05.999 | 10:39:51.000 |  |
| StorageUsage | 3119 | 0.967 | 09:46:06.808 | 10:39:51.839 |  |
| EntityMonitoringState | 3119 | 0.967 | 09:46:06.811 | 10:39:51.842 |  |
| AlignmentState | 3118 | 0.966 | 09:46:06.823 | 10:39:50.823 | yes |
| PathControlState | 3011 | 0.933 | 09:46:10.018 | 10:39:51.124 | yes |
| GpsFixRejection | 2747 | 0.851 | 09:48:11.007 | 10:37:58.996 | yes |
| TransportBindings | 951 | 0.295 | 09:46:05.680 | 09:46:05.687 |  |
| Announce | 670 | 0.208 | 09:46:07.385 | 10:39:47.385 | yes |
| LogBookEntry | 536 | 0.166 | 09:46:05.516 | 10:39:51.851 | yes |
| RSSI | 332 | 0.103 | 09:46:11.603 | 10:39:50.821 |  |
| EntityActivationState | 293 | 0.091 | 09:46:05.776 | 10:39:51.855 | yes |
| ReportControl | 220 | 0.068 | 09:46:13.119 | 10:39:41.462 |  |
| EntityInfo | 125 | 0.039 | 09:46:05.484 | 10:39:51.855 | yes |
| UamTxFrame | 108 | 0.033 | 09:46:13.119 | 10:39:41.463 | yes |
| QueryEntityInfo | 99 | 0.031 | 09:46:05.430 | 09:46:05.430 |  |
| ControlLoops | 42 | 0.013 | 09:46:10.017 | 10:38:01.024 |  |
| VehicleCommand | 27 | 0.008 | 09:46:05.435 | 10:39:51.850 |  |
| SetEntityParameters | 24 | 0.007 | 09:46:05.774 | 10:38:03.517 |  |
| DesiredPath | 14 | 0.004 | 09:46:10.017 | 10:38:04.025 | yes |
| DesiredSpeed | 14 | 0.004 | 09:46:10.018 | 10:38:04.025 | yes |
| DesiredZ | 12 | 0.004 | 09:46:10.018 | 10:38:04.025 | yes |
| EntityList | 10 | 0.003 | 09:46:07.890 | 09:48:07.035 | yes |
| PlanDB | 10 | 0.003 | 09:46:07.890 | 09:48:07.041 |  |
| LblConfig | 10 | 0.003 | 09:46:07.891 | 09:48:07.037 |  |
| RemoteActionsRequest | 10 | 0.003 | 09:46:07.891 | 09:48:07.056 |  |
| IridiumTxStatus | 9 | 0.003 | 10:08:49.509 | 10:39:49.748 |  |
| Goto | 7 | 0.002 | 09:46:10.016 | 10:35:00.018 |  |
| LoggingControl | 3 | 0.001 | 09:46:05.430 | 10:39:51.863 | yes |
| IridiumMsgTx | 3 | 0.001 | 10:08:49.509 | 10:37:57.509 |  |
| Sms | 3 | 0.001 | 10:08:49.509 | 10:37:57.510 |  |
| PushEntityParameters | 2 | 0.001 | 09:46:05.433 | 09:46:05.433 |  |
| YoYo | 2 | 0.001 | 09:49:34.517 | 10:14:22.017 |  |
| PopUp | 2 | 0.001 | 10:08:04.018 | 10:37:40.517 |  |
| PlanGeneration | 2 | 0.001 | 10:10:40.422 | 10:10:40.423 |  |
| PlanControl | 2 | 0.001 | 10:39:52.720 | 10:39:51.850 | yes |
| PopEntityParameters | 2 | 0.001 | 10:39:51.851 | 10:39:51.854 |  |
| PlanSpecification | 1 | 0.000 | 09:46:05.434 | 09:46:05.434 |  |
| OperationalLimits | 1 | 0.000 | 09:43:36.718 | 09:43:36.718 |  |
| StopManeuver | 1 | 0.000 | 09:46:09.516 | 09:46:09.516 |  |
| DvlRejection | 1 | 0.000 | 09:54:48.237 | 09:54:48.237 | yes |
| IridiumMsgRx | 1 | 0.000 | 10:10:40.422 | 10:10:40.422 |  |
| TextMessage | 1 | 0.000 | 10:10:40.422 | 10:10:40.422 | yes |
| StationKeeping | 1 | 0.000 | 10:38:04.018 | 10:38:04.018 |  |
| PlanStatistics | 1 | 0.000 | 10:39:51.856 | 10:39:51.856 |  |

## Source entities per decoded message type

| message | entity id | label | count |
|---|---|---|---|
| Acceleration | 58 | AHRS | 161304 |
| AlignmentState | 47 | Navigation | 3118 |
| AngularVelocity | 58 | AHRS | 161304 |
| Announce | 82 | Service Announcer | 644 |
| Announce | 1 | Motor Controller | 14 |
| Announce | 10 | Text Message Parser | 12 |
| Chlorophyll | 73 | Turner Chlorophyll | 3227 |
| Conductivity | 70 | SmartX | 3227 |
| Depth | 59 | DVL | 16132 |
| Depth | 70 | SmartX | 3227 |
| DesiredHeading | 21 | Path Control | 24904 |
| DesiredPath | 27 | Goto Maneuver | 7 |
| DesiredPath | 35 | Pop Up Maneuver | 4 |
| DesiredPath | 31 | YoYo Maneuver | 2 |
| DesiredPath | 30 | Station Keeping Maneuver | 1 |
| DesiredSpeed | 21 | Path Control | 14 |
| DesiredZ | 22 | Path Control - Bottom Track | 12 |
| Distance | 60 | DVL - Beam 0 | 16132 |
| Distance | 61 | DVL - Beam 1 | 16132 |
| Distance | 62 | DVL - Beam 2 | 16132 |
| Distance | 63 | DVL - Beam 3 | 16132 |
| Distance | 64 | DVL Filtered | 16132 |
| DvlRejection | 47 | Navigation | 1 |
| EntityActivationState | 25 | Multiplexer Maneuver | 72 |
| EntityActivationState | 21 | Path Control | 39 |
| EntityActivationState | 20 | Speed Control | 39 |
| EntityActivationState | 12 | Attitude | 39 |
| EntityActivationState | 11 | Allocator | 39 |
| EntityActivationState | 18 | Diving | 39 |
| EntityActivationState | 98 | SILCAM | 13 |
| EntityActivationState | 48 | LBL Ranger | 13 |
| EntityInfo | 48 | LBL Ranger | 14 |
| EntityInfo | 98 | SILCAM | 14 |
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
| EntityInfo | 24 | Follow Reference Maneuver | 1 |
| EntityInfo | 25 | Multiplexer Maneuver | 1 |
| EntityInfo | 26 | Idle Maneuver | 1 |
| EntityInfo | 27 | Goto Maneuver | 1 |
| EntityInfo | 28 | Launch Maneuver | 1 |
| EntityInfo | 29 | Loiter Maneuver | 1 |
| EntityInfo | 30 | Station Keeping Maneuver | 1 |
| EntityInfo | 31 | YoYo Maneuver | 1 |
| EntityInfo | 32 | Rows Maneuver | 1 |
| EntityInfo | 33 | Follow Path Maneuver | 1 |
| EntityInfo | 34 | Elevator Maneuver | 1 |
| EntityInfo | 5 | Servo Controller | 1 |
| EntityInfo | 6 | Servo Controller - Servo 0 | 1 |
| EntityInfo | 7 | Servo Controller - Servo 1 | 1 |
| EntityInfo | 8 | Servo Controller - Servo 2 | 1 |
| EntityInfo | 9 | Servo Controller - Servo 3 | 1 |
| EntityInfo | 1 | Motor Controller | 1 |
| EntityInfo | 2 | Motor | 1 |
| EntityInfo | 3 | Motor Controller (Bridge) | 1 |
| EntityInfo | 4 | Motor Controller (MCU) | 1 |
| EntityInfo | 35 | Pop Up Maneuver | 1 |
| EntityInfo | 19 | Remote Control | 1 |
| EntityInfo | 36 | Dislodge Maneuver | 1 |
| EntityInfo | 37 | Alignment Maneuver | 1 |
| EntityInfo | 38 | Magnetometer Maneuver | 1 |
| EntityInfo | 39 | Teleoperation Maneuver | 1 |
| EntityInfo | 40 | Collisions | 1 |
| EntityInfo | 41 | Entity Monitor | 1 |
| EntityInfo | 45 | Servo Monitor | 1 |
| EntityInfo | 46 | Tachograph | 1 |
| EntityInfo | 49 | Plan Engine | 1 |
| EntityInfo | 50 | Plan Generator | 1 |
| EntityInfo | 51 | Power Supply | 1 |
| EntityInfo | 52 | Batteries | 1 |
| EntityInfo | 53 | Power Supply (+12VDC) | 1 |
| EntityInfo | 54 | Power Supply (+5VDC) | 1 |
| EntityInfo | 55 | Medium Sensor | 1 |
| EntityInfo | 56 | Leak Sensor | 1 |
| EntityInfo | 57 | GPS | 1 |
| EntityInfo | 58 | AHRS | 1 |
| EntityInfo | 59 | DVL | 1 |
| EntityInfo | 60 | DVL - Beam 0 | 1 |
| EntityInfo | 61 | DVL - Beam 1 | 1 |
| EntityInfo | 62 | DVL - Beam 2 | 1 |
| EntityInfo | 63 | DVL - Beam 3 | 1 |
| EntityInfo | 64 | DVL Filtered | 1 |
| EntityInfo | 47 | Navigation | 1 |
| EntityInfo | 73 | Turner Chlorophyll | 1 |
| EntityInfo | 74 | Turner Turbidity | 1 |
| EntityInfo | 75 | Clock | 1 |
| EntityInfo | 76 | Power Supervisor | 1 |
| EntityInfo | 78 | Report Supervisor | 1 |
| EntityInfo | 83 | Cache | 1 |
| EntityInfo | 18 | Diving | 1 |
| EntityInfo | 87 | GSM | 1 |
| EntityInfo | 89 | Iridium Modem | 1 |
| EntityInfo | 90 | Log Book | 1 |
| EntityInfo | 92 | NMEA | 1 |
| EntityInfo | 93 | TCP Server (Backseat) | 1 |
| EntityInfo | 95 | Acoustic Access Controller | 1 |
| EntityInfo | 94 | TCP Server (Settings) | 1 |
| EntityInfo | 96 | UDP | 1 |
| EntityInfo | 91 | Logger | 1 |
| EntityInfo | 44 | Operational Limits | 1 |
| EntityInfo | 69 | WBT | 1 |
| EntityInfo | 81 | Vehicle Supervisor | 1 |
| EntityInfo | 70 | SmartX | 1 |
| EntityInfo | 71 | SmartX - Analog1 | 1 |
| EntityInfo | 72 | SmartX - Analog2 | 1 |
| EntityInfo | 84 | Service Discovery | 1 |
| EntityInfo | 86 | FTP Server | 1 |
| EntityInfo | 88 | HTTP Server | 1 |
| EntityInfo | 82 | Service Announcer | 1 |
| EntityInfo | 42 | Fuel | 1 |
| EntityInfo | 43 | Medium | 1 |
| EntityInfo | 65 | Mainboard | 1 |
| EntityInfo | 66 | Mainboard (Core) | 1 |
| EntityInfo | 67 | Mainboard (SuperIO) | 1 |
| EntityInfo | 68 | Mainboard (Board) | 1 |
| EntityInfo | 77 | Recovery Supervisor | 1 |
| EntityInfo | 80 | Storage Supervisor | 1 |
| EntityInfo | 79 | Safety Supervisor | 1 |
| EntityInfo | 97 | LEDs | 1 |
| EntityInfo | 85 | Acoustic Modem | 1 |
| EntityList | 1 | Motor Controller | 5 |
| EntityList | 0 | Daemon | 5 |
| EstimatedState | 47 | Navigation | 64528 |
| EulerAngles | 58 | AHRS | 161304 |
| GpsFix | 57 | GPS | 3226 |
| GpsFix | 47 | Navigation | 1 |
| GpsFixRejection | 47 | Navigation | 2747 |
| GroundVelocity | 59 | DVL | 16132 |
| LogBookEntry | 87 | GSM | 340 |
| LogBookEntry | 81 | Vehicle Supervisor | 150 |
| LogBookEntry | 21 | Path Control | 16 |
| LogBookEntry | 49 | Plan Engine | 15 |
| LogBookEntry | 89 | Iridium Modem | 4 |
| LogBookEntry | 79 | Safety Supervisor | 3 |
| LogBookEntry | 96 | UDP | 2 |
| LogBookEntry | 47 | Navigation | 2 |
| LogBookEntry | 50 | Plan Generator | 2 |
| LogBookEntry | 10 | Text Message Parser | 1 |
| LogBookEntry | 30 | Station Keeping Maneuver | 1 |
| LoggingControl | 91 | Logger | 2 |
| LoggingControl | 49 | Plan Engine | 1 |
| MagneticField | 58 | AHRS | 161304 |
| ManeuverControlState | 30 | Station Keeping Maneuver | 4476 |
| ManeuverControlState | 35 | Pop Up Maneuver | 2539 |
| ManeuverControlState | 31 | YoYo Maneuver | 2112 |
| ManeuverControlState | 27 | Goto Maneuver | 736 |
| ManeuverControlState | 26 | Idle Maneuver | 195 |
| ManeuverControlState | 25 | Multiplexer Maneuver | 24 |
| NavigationData | 47 | Navigation | 64528 |
| NavigationUncertainty | 47 | Navigation | 64528 |
| PathControlState | 21 | Path Control | 3011 |
| PlanControl | 7 | Servo Controller - Servo 1 | 1 |
| PlanControl | 49 | Plan Engine | 1 |
| PlanControlState | 49 | Plan Engine | 9231 |
| Pressure | 59 | DVL | 16132 |
| Pressure | 70 | SmartX | 3227 |
| Rpm | 2 | Motor | 32264 |
| Salinity | 70 | SmartX | 3227 |
| SetThrusterActuation | 20 | Speed Control | 31925 |
| SoundSpeed | 59 | DVL | 16132 |
| SoundSpeed | 70 | SmartX | 3227 |
| Temperature | 51 | Power Supply | 18158 |
| Temperature | 59 | DVL | 16132 |
| Temperature | 66 | Mainboard (Core) | 3227 |
| Temperature | 67 | Mainboard (SuperIO) | 3227 |
| Temperature | 68 | Mainboard (Board) | 3227 |
| Temperature | 70 | SmartX | 3227 |
| Temperature | 4 | Motor Controller (MCU) | 1566 |
| Temperature | 3 | Motor Controller (Bridge) | 1566 |
| Temperature | 2 | Motor | 1566 |
| TextMessage | 89 | Iridium Modem | 1 |
| Turbidity | 74 | Turner Turbidity | 3227 |
| UamTxFrame | 95 | Acoustic Access Controller | 108 |
| VehicleMedium | 43 | Medium | 3227 |
| VehicleState | 81 | Vehicle Supervisor | 9252 |
| WaterDensity | 70 | SmartX | 3227 |
| WaterVelocity | 59 | DVL | 16121 |

## Entity table (EntityInfo)

0=Daemon, 1=Motor Controller, 2=Motor, 3=Motor Controller (Bridge), 4=Motor Controller (MCU), 5=Servo Controller, 6=Servo Controller - Servo 0, 7=Servo Controller - Servo 1, 8=Servo Controller - Servo 2, 9=Servo Controller - Servo 3, 10=Text Message Parser, 11=Allocator, 12=Attitude, 13=Roll Parcel, 14=Pitch Parcel, 15=Depth Parcel, 16=Heading Parcel, 17=Heading Rate Parcel, 18=Diving, 19=Remote Control, 20=Speed Control, 21=Path Control, 22=Path Control - Bottom Track, 23=Compass Calibration Maneuver, 24=Follow Reference Maneuver, 25=Multiplexer Maneuver, 26=Idle Maneuver, 27=Goto Maneuver, 28=Launch Maneuver, 29=Loiter Maneuver, 30=Station Keeping Maneuver, 31=YoYo Maneuver, 32=Rows Maneuver, 33=Follow Path Maneuver, 34=Elevator Maneuver, 35=Pop Up Maneuver, 36=Dislodge Maneuver, 37=Alignment Maneuver, 38=Magnetometer Maneuver, 39=Teleoperation Maneuver, 40=Collisions, 41=Entity Monitor, 42=Fuel, 43=Medium, 44=Operational Limits, 45=Servo Monitor, 46=Tachograph, 47=Navigation, 48=LBL Ranger, 49=Plan Engine, 50=Plan Generator, 51=Power Supply, 52=Batteries, 53=Power Supply (+12VDC), 54=Power Supply (+5VDC), 55=Medium Sensor, 56=Leak Sensor, 57=GPS, 58=AHRS, 59=DVL, 60=DVL - Beam 0, 61=DVL - Beam 1, 62=DVL - Beam 2, 63=DVL - Beam 3, 64=DVL Filtered, 65=Mainboard, 66=Mainboard (Core), 67=Mainboard (SuperIO), 68=Mainboard (Board), 69=WBT, 70=SmartX, 71=SmartX - Analog1, 72=SmartX - Analog2, 73=Turner Chlorophyll, 74=Turner Turbidity, 75=Clock, 76=Power Supervisor, 77=Recovery Supervisor, 78=Report Supervisor, 79=Safety Supervisor, 80=Storage Supervisor, 81=Vehicle Supervisor, 82=Service Announcer, 83=Cache, 84=Service Discovery, 85=Acoustic Modem, 86=FTP Server, 87=GSM, 88=HTTP Server, 89=Iridium Modem, 90=Log Book, 91=Logger, 92=NMEA, 93=TCP Server (Backseat), 94=TCP Server (Settings), 95=Acoustic Access Controller, 96=UDP, 97=LEDs, 98=SILCAM

## Requested messages NOT present in this log

AcousticOperation, EstimatedStreamVelocity, GnssHwMon, LblEstimate, LblRangeAcceptance, SatellitesInView, SimulatedState, UamRxFrame, UamRxRange, UamTxRange, UamTxStatus, UsblAngles, UsblAnglesExtended, UsblConfig, UsblFix, UsblFixExtended, UsblModem, UsblPosition, UsblPositionExtended, VelocityDelta
