class LedPanel:
    # single, pan, fan, spread, trim
    CC_LED_BEHAVIOR_RANGE = range(1, 9)
    # control for the value displayed on the LED ring
    # normally no need of that
    # CC_LED_RING_RANGE = range(9, 17)

    UPPER_ROW_NOTE_RANGE = range(0, 8)
    # LOWER_ROW_NOTE_RANGE = range(8, 16)

    # MIDI byte meaning
    NOTEON = 0x90
    NOTEOFF = 0x80
    CC = 0xB0

    def __init__(self, midiout):
        self.midiout = midiout

    # CLASS METHODS #

    def light_preset_led(self, note):
        note -= 8
        # light the preset led, dark others leds of the row
        for led_note in self.UPPER_ROW_NOTE_RANGE:
            if led_note == note:
                self._light(led_note)
            else:
                self._dark(led_note)

    # PRIVATE METHODS #

    def _light(self, led):
        self.midiout.send_message([self.NOTEON, led, 1])

    def _dark(self, led):
        self.midiout.send_message([self.NOTEOFF, led, 0])
