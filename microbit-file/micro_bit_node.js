radio.onReceivedString(function (receivedString) {

    if (receivedString == "handshake") {
        if (state == 0) {
            state = 1
            radio.sendString("enrol=" + control.deviceName())
        }
    } else {
        // basic.showString(receivedString)
        if (state == 1) {
            if (receivedString.includes("call")) {
                basic.showIcon(IconNames.No)
                music.beginMelody(music.builtInMelody(Melodies.Wawawawaa), MelodyOptions.Once)
            } else {
                buffer = receivedString.split('=')
                if (buffer[0] == "mood") {
                    if (buffer[1] == "sad") {
                        basic.showIcon(IconNames.Sad)
                        music.beginMelody(music.builtInMelody(Melodies.BaDing), MelodyOptions.Once)
                        music.beginMelody(music.builtInMelody(Melodies.BaDing), MelodyOptions.Once)
                        music.beginMelody(music.builtInMelody(Melodies.BaDing), MelodyOptions.Once)
                        lightState = 0
                        pins.digitalWritePin(DigitalPin.P0, lightState)
                    } else {
                        basic.showIcon(IconNames.Heart)
                        lightState = 1
                        pins.digitalWritePin(DigitalPin.P0, lightState)
                    }
                } else {
                    basic.showIcon(IconNames.Heart)
                    lightState = 1
                    pins.digitalWritePin(DigitalPin.P0, lightState)
                }
            }
        }
    }
})

input.onButtonPressed(Button.A, function () {
    radio.sendString("call")
})

input.onButtonPressed(Button.B, function () {
    basic.showIcon(IconNames.Yes)
})
let lightState = 0
let state = 0
let buffer: string[] = []
// let flag = 0
radio.setGroup(8)
radio.setTransmitSerialNumber(true)
radio.setTransmitPower(7)
basic.showIcon(IconNames.Giraffe)
basic.forever(function () {
    // basic.showNumber(state)
})
