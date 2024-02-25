# import src.ctl.leds as leds
import src.models.xtouch as xtouch

# fromxtouch = rtmidi.MidiIn()
# toxtouch = rtmidi.MidiOut()
# midiout = rtmidi.MidiOut()


def generate_message(message, prefix):
    if len(message) > 0:
        # Extraction du numéro de canal et du type de message
        status = message[0]
        channel = status & 0xF
        message_type = status & 0xF0

        # Control Change
        if message_type == 0xB0:
            midi_message = f"{prefix} CC - Channel: {channel}, Controller: {message[1]}, Value: {message[2]}"
            return f"{midi_message:<50}"

        # Note ON/OFF
        elif message_type in (0x90,  0x80):
            note_number = message[1]
            velocity = message[2]
            prefix += "ON" if message_type == 0x90 else "OF"
            midi_message = f"{prefix} - Channel: {channel}, Note: {note_number}, Velocity: {velocity}"
            return f"{midi_message:<50}"

        # Other messages
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


# midi_in_ports = fromxtouch.get_ports()

# if midi_in_ports:
#     # Connexion automatique au X-TOUCH MINI
#     xtouchmini_port = next((index for index, port_name in enumerate(midi_in_ports) if "X-TOUCH MINI" in port_name), None)
#     print(f"X-Touch Mini trouvé sur le port MIDI: {xtouchmini_port}.")
#     # fromxtouch.open_port(xtouchmini_port)
#     print(f"Ouverture du port MIDI: {midi_in_ports[xtouchmini_port]}")
# else:
#     print("Aucun port MIDI disponible.")
#     exit()

# midi_out_ports = toxtouch.get_ports()
# if midi_out_ports:
#     # Connexion automatique au X-TOUCH MINI
#     # xtouchmini_port = next((index for index, port_name in enumerate(midi_out_ports) if "X-TOUCH MINI" in port_name), None)
#     # toxtouch.open_port(xtouchmini_port)
# else:
#     print("Aucun X-Touch Mini trouvé.")
#     exit()

# Ouverture d'un port virtuel
# midiout.open_virtual_port("OCGG")


# def led_on(toxtouch):
#     note = 0
#     velocity = 1
#     status = 0x90   # 0x90 = Note ON, add "+ 10" for canal 10
#     note_on = [status, note, velocity]
#     toxtouch.send_message(note_on)


ctl = xtouch.XTouch()
if ctl.midiin is None:
    print("No X-Touch Mini found: check if the device is connected.")
    exit()

# led_on(toxtouch)

print("\nEn attente de signaux...\n")
try:
    input()
    # while True:
    #     fromxtouch_tuple = fromxtouch.get_message()
    #     test = ctl.midiin.get_message()
    #     if test:
    #         print(test)
    #     if fromxtouch_tuple is not None:
    #         # print("\033[2A\033[K", end="")  # Erase 2 lines above, each loop
    #         midi_in, time_stamp = fromxtouch_tuple
    #         print(generate_message(midi_in, 'IN: '))
    #         midi_out = process_message(midi_in)
    #         midiout.send_message(midi_out)
    #         print(generate_message(midi_out, 'OUT:'))
    #     time.sleep(0.002)

except KeyboardInterrupt:
    print("\nArrêt du programme.")

finally:
    ctl.midiin.close_port()
    del ctl
