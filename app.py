# Initialize MIDI connections & verify if x-touch mini is connected
import src.midi_connections as midi
import src.command_line_interface as cli
import src.led_panel as leds
import src.xtouch as xtouch


# DECLARATIONS ################################################################


midiin = midi.create_midiin()           # MIDI from xtouch
midiout = midi.create_midiout()         # MIDI to xtouch (leds management)
virtualout = midi.create_virtualout()   # main MIDI out

# command line view
cli = cli.CommandLineInterface()
# X-Touch physical leds management (physical "view")
leds = leds.LedPanel(midiout)
# main app controller
device = xtouch.XTouch(midiin, virtualout, leds, cli)


# RUN #########################################################################


# run the cli app
# !!! FOR NOW, THIS AND ITS LOOP is the only reason why
# the app gently waits for midi input.
try:
    print('Press CTRL-C to quit')
    cli.run()
except KeyboardInterrupt:
    # dark all leds
    leds.dark_all_upper_leds()
    # close midi ports
    midiin.close_port()
    midiout.close_port()
    virtualout.delete()
