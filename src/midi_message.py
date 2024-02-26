from copy import deepcopy


class MidiMessage:
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

    def is_preset_change(self):
        return self.is_note() and self.knob in range(8, 16)

    def is_from_fader(self):
        return self.is_cc() and self.knob in (9, 10)

    def is_from_layer_b(self):
        if self.is_cc():
            return self.knob in range(10, 19)
        elif self.is_note():
            return self.knob in range(24, 48)

    def translate(self, preset):
        new_msg = deepcopy(self)
        new_msg.source = "virtualout"
        if new_msg.is_cc():
            new_msg.knob += preset['cc_offset']
        elif new_msg.is_note():
            new_msg.knob += preset['note_offset']
        return new_msg

    def to_raw(self):
        # first_byte = (self.msg_type << 4) | self.channel
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
