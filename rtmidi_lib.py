import rtmidi
import time

midiin = rtmidi.MidiIn()
midiout = rtmidi.MidiOut()


def print_message(message, prefix):
    if len(message) > 0:
        # Extraction du numéro de canal et du type de message
        status = message[0]
        channel = status & 0xF
        message_type = status & 0xF0

        # Control Change
        if message_type == 0xB0:
            controller_number = message[1]
            controller_value = message[2]
            midi_message = f"{prefix} CC - Channel: {channel}, Controller: {controller_number}, Value: {controller_value}"
            return f"{midi_message:<50}"

        # Note ON/OFF
        elif message_type in (0x90,  0x80):
            note_number = message[1]
            velocity = message[2] if message_type == 0x90 else 0
            note_status = "O" if message_type == 0x90 else "F"
            midi_message = f"{prefix} N{note_status} - Channel: {channel}, Note: {note_number}, Velocity: {velocity}"
            return f"{midi_message:<50}"

        # Autres types de messages non spécifiés
        else:
            return f"Message non spécifié: {message}"
    else:
        return "Aucun message reçu."


def process_message(message):
    # message[0] : status ?
    # message[1] : note/controller number
    # message[2] : note velocity / controller value

    if message[0] & 0xF0 == 0x90:  # Note ON
        message[2] = 64  # Modifier la vélocité
    return message


available_ports = midiin.get_ports()

if available_ports:
    # Connexion automatique au X-TOUCH MINI
    xtouchmini_port = next((index for index, port_name in enumerate(available_ports) if "X-TOUCH MINI" in port_name), None)
    print(f"X-Touch Mini trouvé sur le port MIDI: {xtouchmini_port}.")
    midiin.open_port(xtouchmini_port)
    print(f"Ouverture du port MIDI: {available_ports[xtouchmini_port]}")
else:
    print("Aucun port MIDI disponible.")
    exit()

available_output_ports = midiout.get_ports()
if available_output_ports:
    midiout.open_port(0)  # Ouvrir le premier port disponible
# else:
#     # Ouverture d'un port virtuel si aucun port physique n'est disponible
#     midiout.open_virtual_port("My virtual output")


print("\nEn attente de signaux...\n")
try:
    while True:
        midiin_tuple = midiin.get_message()
        if midiin_tuple is not None:
            print("\033[2A\033[K", end="")
            midi_in, time_stamp = midiin_tuple
            print(print_message(midi_in, 'IN: '))
            # display = print_message(midi_in, "IN: ")
            midi_out = process_message(midi_in)
            # display += "        " + print_message(midi_out, "OUT:")
            midiout.send_message(midi_out)
            # print("\033[F\033[K", end="")
            print(print_message(midi_out, 'OUT:'))
            # print(f"\r{display}", end="")
        time.sleep(0.002)

except KeyboardInterrupt:
    print("\nArrêt du programme.")

finally:
    midiin.close_port()
    midiout.close_port()
    del midiin
    del midiout
