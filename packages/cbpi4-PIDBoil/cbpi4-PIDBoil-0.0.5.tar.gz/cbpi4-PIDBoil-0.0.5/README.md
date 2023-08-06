# Craftbeerpi4 Kettle Logic Plugin

### PID Logic with boil threshold.

If the target Temperature is above a configurable threshold the PID will be ignored and heater is switched on to the max output value. This is helpful if you use the same kettle for mashing and boiling.

Once the boil threshold temperature is reached, the boil will be done with the max boil output power



### Parameters

	P - proportional value

	I - integral value

	D - derivative value

	SampleTime - 2 or 5 seconds -> how often the logic calculates the power setting

	max output - heater power which is set above boil threshold

	Boil Threshold - Above this temperature the heater will be set to Max Boil Output Power (default: 98°C / 208F)

	Max Boil Output - Power (%) that is used above Boil Threshold Temperature (default: 100%)

### Changelog

- 21.11.21: Adapted to cbpi4 4.0.0.45 to accomodate actor power settings incl. the PWM Actor.
- 13.10.21: Added Power setting for Boil (0.0.4)
- 13.10.21: Improvement of actor toggling in case of 0% or 100% heating (0.0.3)
- 12.10.21: Bug fixing MashStep Automode Issue (0.0.2)
- 19.08.21: Initial commit (0.0.1)
