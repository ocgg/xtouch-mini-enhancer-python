import src.ledpanel as leds
import src.midi_message as midi_message


# This is the main app controller
class XTouch:
    PRESET_CHANGE_RANGE = range(8, 15)

    def __init__(self, midiin, midiout, virtualout, cli):
        # MIDI CONNECTIONS #
        self.midiin = midiin
        self.midiout = midiout
        self.virtualout = virtualout

        # led controls on the physical xtouch
        self.leds = leds.LedPanel()

        self.cli = cli
        # callback on midi message received
        midiin.set_callback(self.midiin_callback)

        # TODO:signal routing (preset change, etc)
        self.current_preset = self.set_current_preset(1)

    # CLASS METHODS #

    def set_current_preset(self, preset):
        print('TODO: XTouch.set_current_preset()')
        # set offset for CC, CCNotes & buttons
        # light the right leds

    def midiin_callback(self, midi_data, data):
        # Convert midi_data to MidiMessage
        msg = midi_message.MidiMessage(midi_data, "midiin")

        # Send to CLI for display
        self.cli.midiin_msg = msg

        # TODO: signal routing
        # if preset change (NOFF 8-15)
        # do plenty (leds, offset change, etc)
        # if NOFF or CC used, route signal
        # self.route(midi_data)

    # PRIVATE METHODS #
