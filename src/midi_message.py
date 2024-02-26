from copy import deepcopy


class MidiMessage:
    PRESET_CHANGE_RANGE = range(8, 16)   # last range arg is excluded

    LAYER_A_CC_RANGE = range(1, 9)
    LAYER_B_CC_RANGE = range(10, 19)
    LAYER_A_NOTE_RANGE = range(0, 24)
    LAYER_B_NOTE_RANGE = range(24, 48)
    # cc note : note message from a click on cc knob
    LAYER_A_CC_NOTE_RANGE = range(0, 8)
    # unused but left there as a reminder
    # LAYER_B_CC_NOTE_RANGE = range(24, 32)

    def __init__(self, raw_msg, source):
        # TODO:better way to handle MidiMessage:first_byte
        # keep first_byte unchanged (keep channel & type)
        self.first_byte = raw_msg[0][0]
        decrypted = self._decrypt(raw_msg)
        self.channel = decrypted['channel']
        self.msg_type = decrypted['type']
        self.knob = decrypted['knob']
        self.value = decrypted['value']
        self.source = source

    # CLASS METHODS #

    def is_note(self):
        return self.msg_type in ("NOTEON", "NOTEOFF")

    def is_cc(self):
        return self.msg_type == "CC"

    def is_layer_A_cc_note(self):
        return self.is_note() and self.knob in self.LAYER_A_CC_NOTE_RANGE

    def is_layer_A_cc(self):
        return self.is_cc() and self.knob in self.LAYER_A_CC_RANGE

    def is_preset_change(self):
        return self.is_note() and self.knob in self.PRESET_CHANGE_RANGE

    def is_from_layer_B(self):
        if self.is_cc():
            return self.knob in self.LAYER_B_CC_RANGE
        elif self.is_note():
            return self.knob in self.LAYER_B_NOTE_RANGE

    def translate(self, preset):
        new_msg = deepcopy(self)
        new_msg.source = "virtualout"
        if new_msg.is_cc():
            new_msg.knob += preset['cc_offset']
        elif new_msg.is_note():
            new_msg.knob += preset['note_offset']
        return new_msg

    def to_raw(self):
        return [self.first_byte, self.knob, self.value]

    # PRIVATE METHODS #

    def _get_msg_type(self):
        match self.first_byte & 0xF0:
            case 0xB0: return "CC"
            case 0x90: return "NOTEON"
            case 0x80: return "NOTEOFF"
            case _: return "UNKNOWN"

    # Translate data in a more readable way
    def _decrypt(self, raw_msg):
        msg = raw_msg[0]
        return {
            'channel': self.first_byte & 0xF,
            'type': self._get_msg_type(),
            'knob': msg[1],
            'value': msg[2]
        }
