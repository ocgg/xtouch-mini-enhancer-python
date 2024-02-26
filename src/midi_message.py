class MidiMessage:
    def __init__(self, raw_msg, source):
        decrypted = self._decrypt(raw_msg)
        self.channel = decrypted['channel']
        self.msg_type = decrypted['type']
        self.knob = decrypted['knob']
        self.value = decrypted['value']
        self.source = source

    def to_raw(self):
        first_byte = (self.msg_type << 4) | self.channel
        return [first_byte, self.knob, self.value]

    # PRIVATE METHODS #

    def _get_msg_type(self, first_byte):
        match first_byte & 0xF0:
            case 0xB0: return "CC"
            case 0x90: return "NOTEON"
            case 0x80: return "NOTEOFF"
            case _: return "UNKNOWN"

    # Translate data in a more readable way
    def _decrypt(self, midi_data):
        msg = midi_data[0]
        first_byte = msg[0]
        return {
            'channel': first_byte & 0xF,
            'type': self._get_msg_type(first_byte),
            'knob': msg[1],
            'value': msg[2]
        }
