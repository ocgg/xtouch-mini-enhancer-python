class LedPanel:
    # single, pan, fan, spread, trim
    CC_LED_BEHAVIOR_RANGE = range(1, 9)
    # control for the value displayed on the LED ring
    # normally no need of that
    # CC_LED_RING_RANGE = range(9, 17)

    UPPER_ROW_NOTE_RANGE = range(0, 8)
    # LOWER_ROW_NOTE_RANGE = range(8, 16)

    def __init__(self, midiout):
        self.midiout = midiout

    def led_on():
        note = 0
        velocity = 1
        status = 0x90   # 0x90 = Note ON, add "+ 10" for canal 10
        note_on = [status, note, velocity]
        self.midiout.send_message(note_on)
