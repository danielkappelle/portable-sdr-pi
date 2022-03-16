# Portable SDR Pi
A portable SDR solution to listen to anything from FM radio to airband.

The setup looks as follows
![The setup](./setup-poc.jpeg)

## ISSUES
- Changing from WBFM to AM does not work over the UDP port
  - Fix: best option is probably to kill the process when switching between modes and then start a new process with the proper settings. This also paves the way for the marine VHF where we will have to scan multiple frequencies (duplex).
## Feature ideas
- Possibility to use presets
  - Airband (quickly jump to right frequency range)
  - ~Airband presets for certain airports~
  - Marine VHF radio (channel presets)
  - ~27 MHz Citizens band channel presets~
  - Motorola walkie talkie channels
- More decoding functionality
  - VOR decoding
  - RDS decoding

On the hardware side
- Neat enclosure
- Proper controls, multiple knobs and proper screen
- Little audio amplifier and built-in speakers
- Possibilty to plug into 12V adapter, or maybe via USB (for use in car)
