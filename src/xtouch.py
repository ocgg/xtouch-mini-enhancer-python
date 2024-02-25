import src.command_line_interface as cli
import src.ledpanel as leds


# This is the main app controller
class XTouch:
    def __init__(self, midiin, midiout, virtualout):
        self.midiin = midiin
        self.midiout = midiout
        self.virtualout = virtualout

        # set callbacks
        midiin.set_callback(self.midiin_callback)
        midiin.set_error_callback(self.midiin_error_callback)

        # instanciate 2 elements like views:
        # - the Interface class (terminal view)
        # - the LedPanel class (leds displaying on the physical device)
        # self.cli = cli.CommandLineInterface()
        # self.leds = leds.LedPanel()

    def midiin_callback(midi_msg, data):
        print(midi_msg)
        # self.cli.print_midi_data(message)

    def midiin_error_callback(midi_msg, data):
        print('ERROR CALLBACK')
        # self.cli.print_midi_data(message)
