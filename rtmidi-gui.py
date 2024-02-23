import rtmidi
import time
import tkinter as tk

# Création d'une instance de RtMidiIn
midiin = rtmidi.MidiIn()

# Affichage des ports MIDI disponibles et ouverture du premier port disponible
available_ports = midiin.get_ports()
if available_ports:
    midiin.open_port(3)
    print(f"Ouverture du port MIDI: {available_ports[3]}")
else:
    print("Aucun port MIDI disponible.")
    exit()

# Fonction pour afficher les messages MIDI dans la GUI
def print_message(message):
    # Vous pouvez modifier cette fonction pour afficher les messages de manière appropriée
    # dans votre GUI. Par exemple, ajouter le message à une liste ou à un widget de texte.
    if len(message) >  0:
        # Extraction du numéro de canal et du type de message
        status = message[0]
        channel = status &  0xF
        message_type = status &  0xF0

        # Message de contrôle (Control Change)
        if message_type ==  0xB0:
            controller_number = message[1]
            controller_value = message[2]
            return f"CC - Channel: {channel}, Controller: {controller_number}, Value: {controller_value}\n"
        
        # Message de note ON/OFF
        elif message_type in (0x90,  0x80):
            note_number = message[1]
            velocity = message[2] if message_type ==  0x90 else  0
            note_status = "O" if message_type ==  0x90 else "F"
            return f"N{note_status} - Channel: {channel}, Note: {note_number}, Velocity: {velocity}\n"
        
        # Autres types de messages non spécifiés
        else:
            return f"Message non spécifié: {message}\n"
    else:
        return "Aucun message reçu.\n"

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Interface MIDI")

# Widget de texte pour afficher les messages MIDI
message_display = tk.Label(root, text="", font=("Hack",  14))
message_display.pack(pady=10, padx=10)

# Boucle pour lire les messages MIDI entrants et les afficher dans la GUI
def read_midi_messages():
    while True:
        message_with_time = midiin.get_message()
        if message_with_time is not None:
            message, time_stamp = message_with_time
            midi_data = print_message(message)
            message_display.configure(text=midi_data)
        time.sleep(0.002) # Petit délai pour éviter le surcharge du processeur

# Lancement de la boucle de lecture des messages MIDI dans un thread séparé
import threading
threading.Thread(target=read_midi_messages).start()

# Lancement de la boucle principale de l'application Tkinter
root.mainloop()
