###############################################################################
# LED MANAGEMENT WITH THE X-TOUCH MINI
#
# You can send MIDI data to the X-Touch to control the LEDs.
# The MIDI message has to be sent to the "global channel" (channel 0).
#
# BUTTONS LIGHTING
# upper row: notes 0-7; lower row: notes 8-15
# note on (note off also works for LED off)
# Possible velo.:   0 LED off, 1 LED on, 2 LED blinking
#
# ENCODER'S LED RING BEHAVIOR
# CC 1-8
# Possible values:  0 single, 1 pan, 2 fan, 3 spread, 4 trim
#
# ENCODER'S LED RING Value
# CC 9-16
# Possible values:  0 all off, 1-13 LED on, 14-26 LED blinking,
#                   27 all on, 28 all blinking
###############################################################################


class LedPanel:
    CC_LED_BEHAVIOR_RANGE = range(1, 9)
    # CC_LED_RING_RANGE = range(9, 17)      # unused but it's here
    UPPER_ROW_NOTE_RANGE = range(0, 8)
    # LOWER_ROW_NOTE_RANGE = range(8, 16)   # unused but it's here

    # MIDI's readable bytes
    NOTEON = 0x90
    NOTEOFF = 0x80
    CC = 0xB0

    def __init__(self, midiout):
        self.midiout = midiout

    # CLASS METHODS #

    def light_preset_led(self, note):
        note -= 8
        # light the preset led, dark the others
        for led_note in self.UPPER_ROW_NOTE_RANGE:
            if led_note == note:
                self._light(led_note)
            else:
                self._dark(led_note)

    def dark_all_upper_leds(self):
        for led_note in self.UPPER_ROW_NOTE_RANGE:
            self._dark(led_note)

    # PRIVATE METHODS #

    def _light(self, led):
        self.midiout.send_message([self.NOTEON, led, 1])

    def _dark(self, led):
        self.midiout.send_message([self.NOTEOFF, led, 0])
