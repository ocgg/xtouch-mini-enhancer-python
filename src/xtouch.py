import src.ledpanel as leds


# This is the main app controller
class XTouch:
    def __init__(self, midiin, midiout, virtualout, cli):
        # MIDI connections
        self.midiin = midiin
        self.midiout = midiout
        self.virtualout = virtualout

        # led controls on the physical xtouch
        self.leds = leds.LedPanel()

        self.cli = cli
        # callback on midi message received
        midiin.set_callback(self.midiin_callback)

    def midiin_callback(self, midi_msg, data):
        self.cli.midiin_msg = midi_msg
