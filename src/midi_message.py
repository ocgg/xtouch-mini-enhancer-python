class MidiMessage:
    def __init__(self, raw_msg, source):
        # keep first_byte unchanged (keep channel & type)
        self.first_byte = raw_msg[0][0]
        decrypted = self._decrypt(raw_msg)
        self.channel = decrypted['channel']
        self.msg_type = decrypted['type']
        self.knob = decrypted['knob']
        self.value = decrypted['value']
        self.source = source

    # CLASS METHODS #

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
