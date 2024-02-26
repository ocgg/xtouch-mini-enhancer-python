import src.ledpanel as leds
import src.midi_message as midi_message


# This is the main app controller
class XTouch:
    PRESETS = [
        {'cc_offset': 0,    'note_offset': 0},
        {'cc_offset': 18,   'note_offset': 48},
        {'cc_offset': 26,   'note_offset': 56},
        {'cc_offset': 34,   'note_offset': 64},
        {'cc_offset': 42,   'note_offset': 72},
        {'cc_offset': 50,   'note_offset': 80},
        {'cc_offset': 58,   'note_offset': 88},
        {'cc_offset': 66,   'note_offset': 96}
    ]

    def __init__(self, midiin, midiout, virtualout, cli):
        # MIDI CONNECTIONS #
        self.midiin = midiin
        self.midiout = midiout
        self.virtualout = virtualout

        # led controls on the physical xtouch
        self.leds = leds.LedPanel()

        self.cli = cli
        self.current_preset = self.PRESETS[0]
        # callback on midi message received
        midiin.set_callback(self.midiin_callback)

    # CLASS METHODS #

    def midiin_callback(self, raw_msg, data):
        # Convert midi_data to MidiMessage
        msg = midi_message.MidiMessage(raw_msg, "midiin")

        # Send to CLI for display
        self.cli.midiin_msg = msg

        # if preset change (on NOFF 8-15), no virtual output
        if msg.is_preset_change():
            if msg.msg_type == "NOTEOFF":
                self.current_preset = self.PRESETS[msg.knob - 8]
        # TODO: Do not translate fader or layerB messages
        elif msg.is_from_fader() or msg.is_from_layer_b():
            # translate without offset (juste change msg.source)
            translated_msg = msg.translate(self.PRESETS[0])
            self.cli.virtualout_msg = translated_msg
            self.virtualout.send_message(msg.to_raw())
        else:
            translated_msg = msg.translate(self.current_preset)
            self.cli.virtualout_msg = translated_msg
            self.virtualout.send_message(translated_msg.to_raw())

    # PRIVATE METHODS #
