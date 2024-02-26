import src.ledpanel as leds
import src.midi_message as midi_message
import src.preset as preset


# This is the main app controller
class XTouch:
    PRESET_CHANGE_RANGE = range(8, 16)   # 16 is excluded
    PRESETS = [
        # id, cc range, note range, cc offset, note offset, trigger note
        preset.Preset(1, range(1, 8), range(0, 7), 0, 0, 8),
        preset.Preset(2, range(19, 26), range(48, 55), 18, 48, 9),
        preset.Preset(3, range(27, 34), range(56, 63), 26, 56, 10),
        preset.Preset(4, range(35, 42), range(64, 71), 34, 64, 11),
        preset.Preset(5, range(43, 50), range(72, 79), 42, 72, 12),
        preset.Preset(6, range(51, 58), range(80, 87), 50, 80, 13),
        preset.Preset(7, range(59, 66), range(88, 95), 58, 88, 14),
        preset.Preset(8, range(67, 74), range(96, 103), 66, 96, 15)
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

        # TODO:signal routing (preset change, etc)

    # CLASS METHODS #

    # Preset set offset for CC, CCNotes
    def set_current_preset(self, preset_id):
        self.current_preset = self.PRESETS[preset_id - 1]

    def midiin_callback(self, raw_msg, data):
        # Convert midi_data to MidiMessage
        msg = midi_message.MidiMessage(raw_msg, "midiin")

        # Send to CLI for display
        self.cli.midiin_msg = msg

        # if preset change (NOFF 8-15)
        if msg.msg_type in ("NOTEON", "NOTEOFF") and msg.knob in self.PRESET_CHANGE_RANGE:
            if msg.msg_type == "NOTEOFF":
                self.set_current_preset(msg.knob - 7)
        else:
            translated_msg = self.current_preset.translate(msg)
            self.cli.virtualout_msg = translated_msg
            self.virtualout.send_message(translated_msg.to_raw())
        # if NOFF or CC used, route signal
        # self.route(midi_data)

    # PRIVATE METHODS #
