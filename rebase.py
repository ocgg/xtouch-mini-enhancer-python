# Initialize MIDI connections & verify if x-touch mini is connected
import src.midi_connections as midi
import src.xtouch as xtouch

# Instantiation of our main controller
device = xtouch.XTouch(midi.midi_in, midi.midi_out, midi.virtual_out)

print(device.midiin.is_port_open())
input()

# DO NOT FORGET !
print("TODO: close midi ports when app is closed")
