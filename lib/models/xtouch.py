import rtmidi


class XTouch:
    def __init__(self):
        self.midiin = self.init()

    def midiin_callback(self, message, data):
        prefix = "\rIN:"
        # Extraction du numéro de canal et du type de message
        message = message[0]
        status = message[0]
        channel = status & 0xF
        message_type = status & 0xF0

        # Control Change
        if message_type == 0xB0:
            midi_message = f"{prefix} CH:{channel}, CC:{message[1]}, VAL:{message[2]}"
            print(f"{midi_message:<30}", end="")

        # Note ON/OFF
        elif message_type in (0x90,  0x80):
            onoff = "ON" if message_type == 0x90 else "OFF"
            midi_message = f"{prefix} CH:{channel}, N{onoff}:{message[1]}, VEL:{message[2]}"
            print(f"{midi_message:<30}", end="")

        # Other messages
        else:
            print(f"IN:inconnu: {message}", end="")

    def init(self):
        midiin = rtmidi.MidiIn()
        ports = midiin.get_ports()
        port = next((index for index, port_name in enumerate(ports) if "X-TOUCH MINI" in port_name), None)
        midiin.open_port(port)
        midiin.set_callback(self.midiin_callback)
        return midiin
