class MidiMessage:
    def __init__(self, midi_data, source):
        self.source = source
        decrypted = self._decrypt(midi_data)
        self.channel = decrypted['channel']
        self.msg_type = decrypted['type']

        self.knob = decrypted['knob']
        self.value = decrypted['value']

    # PRIVATE METHODS #

    def _get_msg_type(self, first_byte):
        match first_byte & 0xF0:
            case 0xB0: return "CC"
            case 0x90: return "NOTEON"
            case 0x80: return "NOTEOFF"
            case _: return "UNKNOWN"

    def _decrypt(self, midi_data):
        msg = midi_data[0]
        first_byte = msg[0]
        channel = first_byte & 0xF
        msg_type = self._get_msg_type(first_byte)
        return {
            'channel': channel,
            'type': msg_type,
            'knob': msg[1],
            'value': msg[2]
        }
