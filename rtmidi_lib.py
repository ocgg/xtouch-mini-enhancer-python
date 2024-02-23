import rtmidi
import time

midiin = rtmidi.MidiIn()

available_ports = midiin.get_ports()
if available_ports:
    midiin.open_port(3)
    print(f"Ouverture du port MIDI: {available_ports[3]}")
else:
    print("Aucun port MIDI disponible.")
    exit()

def print_message(message):
    if len(message) >  0:
        # Extraction du numéro de canal et du type de message
        status = message[0]
        channel = status &  0xF
        message_type = status &  0xF0

        # Message de contrôle (Control Change)
        if message_type ==  0xB0:
            controller_number = message[1]
            controller_value = message[2]
            print(f"CC - Channel: {channel}, Controller: {controller_number}, Value: {controller_value}")
        
        # Message de note ON/OFF
        elif message_type in (0x90,  0x80):
            note_number = message[1]
            velocity = message[2] if message_type ==  0x90 else  0
            note_status = "O" if message_type ==  0x90 else "F"
            print(f"N{note_status} - Channel: {channel}, Note: {note_number}, Velocity: {velocity}")
        
        # Autres types de messages non spécifiés
        else:
            print(f"Message non spécifié: {message}")
    else:
        print("Aucun message reçu.")

try:
    while True:
        message_with_time = midiin.get_message()
        if message_with_time is not None:
            message, time_stamp = message_with_time
            print_message(message)
        time.sleep(0.002)
except KeyboardInterrupt:
    print("Arrêt du programme.")
finally:
    midiin.close_port()
    del midiin
