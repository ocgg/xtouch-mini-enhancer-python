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

    def translate(self, preset):
        new_msg = deepcopy(self)
        new_msg.source = "virtualout"
        if new_msg.msg_type == "CC":
            new_msg.knob += preset.cc_offset
        elif new_msg.msg_type in ("NOTEON", "NOTEOFF"):
            new_msg.knob += preset.note_offset
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
