from copy import deepcopy


class Preset:
    def __init__(self, id, cc_offset, note_offset):
        self.id = id
        self.cc_offset = cc_offset
        self.note_offset = note_offset

    def translate(self, msg):
        new_msg = deepcopy(msg)
        new_msg.source = "virtualout"

        if new_msg.msg_type == "CC":
            new_msg.knob += self.cc_offset
        elif new_msg.msg_type in ("NOTEON", "NOTEOFF"):
            new_msg.knob += self.note_offset

        return new_msg
