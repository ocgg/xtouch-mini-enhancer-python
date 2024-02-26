import time


class CommandLineInterface:
    def __init__(self):
        print("TODO:Callback on CLI:midiin_msg change")
        self.midiin_msg = None
        self.virtualout_msg = None

    # Main loop
    def run(self):
        print("\nWaiting MIDI from X-Touch...\n")
        while True:
            if self.midiin_msg is not None and self.virtualout_msg is not None:
                # Erase 2 lines above, each loop
                print("\033[2A\033[K", end="")
                print(self._stringify_msg(self.midiin_msg))
                print(self._stringify_msg(self.virtualout_msg))
            time.sleep(0.01)

    # Generate the message to print
    def _stringify_msg(self, msg):
        prefix = "\rIN: " if msg.source == "midiin" else "\rOUT:"
        if msg.msg_type in ('NOTEON', 'NOTEOFF'):
            val = f"VEL:{msg.value}"
        else:
            val = f"VAL:{msg.value}"
        string = f"{prefix} CH:{msg.channel}, {msg.msg_type}:{msg.knob}, {val}"
        return f"{string:35}"
