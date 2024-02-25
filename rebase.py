# Initialize MIDI connections & verify if x-touch mini is connected
import src.midi_connections as midi
import src.xtouch as xtouch

import src.command_line_interface as cli


# DECLARATIONS ################################################################


midiin = midi.create_midiin()           # MIDI from xtouch
midiout = midi.create_midiout()         # MIDI to xtouch (leds management)
virtualout = midi.create_virtualout()   # main MIDI out

# command line view
cli = cli.CommandLineInterface()

# main app controller
device = xtouch.XTouch(midiin, midiout, virtualout, cli)


# RUN #########################################################################


# run the cli app
# !!! FOR NOW, THIS AND ITS LOOP is the only reason why
# the app gently waits for midi input.
cli.run()


# CLEANUP #####################################################################


# DO NOT FORGET !
print("TODO: close midi ports when app is closed")
