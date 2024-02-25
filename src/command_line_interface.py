import time


class CommandLineInterface:
    CONTROL_CHANGE = 0xB0
    NOTE_ON = 0x90
    NOTE_OFF = 0x80

    def __init__(self):
        self.midiin_msg = None
        self.midiout_msg = None

    def run(self):
        print("TODO:CommandLineInterface main_loop")
        print("\nEn attente de signaux...\n")
        # input()
        while True:
            if self.midiin_msg is not None:
                # Erase 2 lines above, each loop
                print("\033[2A\033[K", end="")
                print(self.midiin_msg, end="")
            time.sleep(0.002)

    def update_midiin_msg(self, midi_msg):
        print(midi_msg)
        self.midiin_msg = midi_msg

    def update_midiout_msg(self, midi_msg):
        self.midiout_msg = midi_msg

    def print_midi_data(self, data):
        prefix = "\rIN:"
        # Extraction of channel number and midi message type
        midi_msg = data[0]
        status = midi_msg[0]
        # "& 0xF": bitwise AND operation to extract the last 4 bits (LSB)
        channel = f"CH:{status & 0xF}"

        msg_to_print = f"{prefix} {channel}, "

        # "& 0xF0": bitwise AND operation to extract the first 4 bits (MSB)
        midi_msg_type = status & 0xF0

        # Control Change
        if midi_msg_type == self.CONTROL_CHANGE:
            controller = f"CC:{midi_msg[1]}"
            value = f"VAL:{midi_msg[2]}"
            msg_to_print += f"{controller}, {value}"
            print(f"{msg_to_print:<30}", end="")

        # Note ON/OFF
        elif midi_msg_type in (self.NOTE_ON,  self.NOTE_OFF):
            onoff = "ON" if midi_msg_type == 0x90 else "OFF"
            note = f"N{onoff}:{midi_msg[1]}"
            velocity = f"VEL:{midi_msg[2]}"
            msg_to_print += f"{note}, {velocity}"
            print(f"{msg_to_print:<30}", end="")

        # Other midi messsages
        else:
            print(f"{msg_to_print}, unknown: {midi_msg}", end="")
