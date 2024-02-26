import src.ledpanel as leds
import src.midi_message as midi_message


# This is the main app controller
class XTouch:
    # NOTE : As the notes 8-15 are kept for preset change,
    # they are unused for the virtual output
    PRESETS = [
        {'cc_offset': 00,   'note_offset': 00},
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

        # Translate ONLY CC & CCnote from layer A
        if msg.is_layer_A_cc() or msg.is_layer_A_cc_note():
            translated_msg = msg.translate(self.current_preset)
            self._display_and_send(translated_msg)
        # no virtual output if msg is preset change (notes 8-15)
        elif msg.is_preset_change():
            # change preset on noteoff (else do nothing)
            if msg.msg_type == "NOTEOFF":
                self.current_preset = self.PRESETS[msg.knob - 8]
        # Do not translate any other message
        else:
            # this only change msg.source (does not apply offset)
            translated_msg = msg.translate(self.PRESETS[0])
            self._display_and_send(translated_msg)

    # PRIVATE METHODS #

    def _display_and_send(self, msg):
        self.cli.virtualout_msg = msg
        self.virtualout.send_message(msg.to_raw())
