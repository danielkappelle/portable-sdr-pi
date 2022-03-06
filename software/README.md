# Software
This is where the software will be

Scroll through demod types, which includes the presets
- AM
- WBFM
- Airband (basically AM, but bounded frequency range)
- Marine VHF (dual frequencies, should be possible with rfl_fm)
- Citizens Band

Tune frequency/select channel.

For now only one rotary knob, later upgrade to 2 or more

## Display class
Takes care of the display, i.e. creates the image and also updates the display.

Needs to know: current mode, current frequency/channel, wat is currently being edited.

## Input class
Takes care of user input, i.e. knob/button interaction and calls the necessary functions.

## Core class
Is the single source of truth, keeps track of the current settings and propagates the settings to the rtl_fm instance. Probably has a config struct/class or maybe dictionary that it can deliver to the display class so it knows how to update the screen.