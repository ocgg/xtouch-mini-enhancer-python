import rtmidi


# FUNCTIONS ###################################################################


# Handling errors
def xtouch_not_found():
    return "No X-Touch Mini found: check if the device is connected."


# Automatic connection to the X-Touch Mini if found
def find_port(midi):
    ports = midi.get_ports()
    if ports:
        port = next(
            (index for index, port_name in enumerate(ports)
                if "X-TOUCH MINI" in port_name), None)
        return port if port else None


# Initialize MIDI connections
def init_midi(midi):
    port = find_port(midi)
    midi.open_port(port) if port else exit(xtouch_not_found())
    return midi


# MAIN ########################################################################


def create_midiin():
    midi = init_midi(rtmidi.MidiIn())
    midi.ignore_types(False, False, False)
    return midi


def create_midiout():
    return init_midi(rtmidi.MidiOut())


def create_virtualout():
    virtual_out = rtmidi.MidiOut()
    virtual_out.open_virtual_port("OCGG")
    return virtual_out
