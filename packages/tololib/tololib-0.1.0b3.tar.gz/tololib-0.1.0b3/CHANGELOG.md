# Changelog

## v0.1.0b3

  * Added Python 3.10 support
  * Added client method `lamp_change_color`
  * Added `water_level_percent` property for `StatusInfo`

## v0.1.0b2

  * Renamed unused `Calefaction.UNCLEAR2` to `Calefaction.UNCLEAR` (last unclear value in this enum) 
  * Fixed typing annotations
  * Improved definition of `STATUS` and `SETTINGS` commands

## v0.1.0b1

  * New CLI sub-command `show-status`
  * Added exception `ResponseTimedOutError` to signal timed out updates
  * Fixed integer boundaries for `STATUS` command (seems to b 0 when sending, 17 when receiving)
  * Fixed integer boundaries for `SETTINGS` command (seems to b 0 when sending, 8 when receiving)
  * Improved exception on command parsing errors

## v0.1.0a6

  * Improved simulator behavior, added first tests
  * Fixed bug polling salt bath timer status
  * Fixed `unlimited` special value for power timer
  * Fixed errors on 0 value for timers
  * Added test for `Command.from_code`

## v0.1.0a5

  * Allow more relaxed and realistic values for current temperature/humidity (range 0..100)

## v0.1.0a4

  * Added Python wheel support
  * Improved server message handling
  * First simulator logic for server
  * Client setter commands

## v0.1.0a3

  * Marked package as PEP561 compatible

## v0.1.0a2

  * Improved documentation
  * Added methods for requesting server status/settings

## v0.1.0a1

  * Created `tololib` project
