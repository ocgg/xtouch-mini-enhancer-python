import time


class CommandLineInterface:
    CONTROL_CHANGE = 0xB0
    NOTE_ON = 0x90
    NOTE_OFF = 0x80

    def __init__(self):
        self.midiin_msg = None
        self.virtualout_msg = None

    # Main loop
    def run(self):
        print("TODO:Callback on midiin_msg change")
        print("\nWaiting MIDI from X-Touch...\n")
        while True:
            if self.midiin_msg is not None:
                # Erase 2 lines above, each loop
                print("\033[2A\033[K", end="")
                print(self._print_midi_data(self.midiin_msg))
                print('TODO: print virtual output')
            time.sleep(0.01)

    # Generate the message to print
    def _print_midi_data(self, data):
        prefix = "\rIN:"
        # Extraction of channel number and midi message type
        midi_msg = data[0]
        status = midi_msg[0]
        # "& 0xF": bitwise AND operation to extract the last 4 bits (LSB)
        channel = f"CH:{status & 0xF}"
        # "& 0xF0": bitwise AND operation to extract the first 4 bits (MSB)
        midi_msg_type = status & 0xF0
        msg_to_print = f"{prefix} {channel}, "

        if midi_msg_type == self.CONTROL_CHANGE:
            controller = f"CC:{midi_msg[1]}"
            value = f"VAL:{midi_msg[2]}"
            msg_to_print += f"{controller}, {value}"

        elif midi_msg_type in (self.NOTE_ON,  self.NOTE_OFF):
            onoff = "ON " if midi_msg_type == self.NOTE_ON else "OFF"
            note = f"NOTE{onoff}:{midi_msg[1]}"
            velocity = f"VEL:{midi_msg[2]}"
            msg_to_print += f"{note}, {velocity}"

        else:
            msg_to_print += f"unknown: {midi_msg}"

        return f"{msg_to_print:<30}"
