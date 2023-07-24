serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    data = serial.readLine()
    data = data.trim()
    // basic.showString(data)
    if (data == "handshake") {
        if (state == 0) {
            state = 1
            radio.sendString("handshake")
            handshakeStartTime = input.runningTime()
        }
        // else {
        //     basic.showNumber(3)
        // }
    } else if (data.includes('cmd:')) {
        music.stopMelody(MelodyStopOptions.All)
        newdata = data.substr(4)
        if (state == 2) {
            preBuffer = newdata.split(",")
            buffer = preBuffer[0].split("=")
            if (buffer[0] == "m") {
                if (buffer[1] == "sad") {
                    buffer = preBuffer[1].split('=')
                    radio.sendString("mood=sad")
                    if (buffer[0] == 's') {
                        basic.showIcon(IconNames.Sad)
                        if (buffer[1] == 'E') {
                            music.beginMelody(music.builtInMelody(Melodies.Entertainer), MelodyOptions.Forever)
                        } else if (buffer[1] == 'W') {
                            music.beginMelody(music.builtInMelody(Melodies.Wedding), MelodyOptions.Forever)
                        } else if (buffer[1] == 'P') {
                            music.beginMelody(music.builtInMelody(Melodies.Prelude), MelodyOptions.Forever)
                        } else if (buffer[1] == 'O') {
                            music.beginMelody(music.builtInMelody(Melodies.Ode), MelodyOptions.Forever)
                        } else {
                            music.beginMelody(music.builtInMelody(Melodies.Chase), MelodyOptions.Forever)
                        }
                    }
                } else if (buffer[1] == "angry") {
                    basic.showIcon(IconNames.Angry)
                    radio.sendString("mood=angry")
                    music.beginMelody(music.builtInMelody(Melodies.PowerUp), MelodyOptions.Once)
                } else {
                    music.stopMelody(MelodyStopOptions.All)
                    basic.showIcon(IconNames.Happy)
                    radio.sendString("nothing")
                }
            }
            // else {
            //     basic.showNumber(4)
            // }
        }
        // else {
        //     basic.showNumber(5)
        // }
    }
    else {
        basic.showNumber(6)
    }
})

input.onButtonPressed(Button.A, function () {
    radio.sendString("call")
})

input.onButtonPressed(Button.B, function () {
    basic.showIcon(IconNames.Yes)
})

radio.onReceivedString(function (receivedString) {
    if (receivedString.includes('call')) {
        basic.showIcon(IconNames.No)
        // basic.showString("Hello")
        music.beginMelody(music.builtInMelody(Melodies.Wawawawaa), MelodyOptions.Once)
    } else if (receivedString.includes('enrol=')) {
        if (state == 1) {
            buffer = receivedString.split('=')
            microbitDevices.push(buffer[1])
        }
    }
})

let response = ""
let microbitDevices: string[] = []
// let sensorValues: string[] = []
let handshakeStartTime = 0
let state = 0
let data = ""
let newdata = ""
let buffer: string[] = []
// let buffer: string
let preBuffer: string[] = []
// let flag = 0
radio.setGroup(8)
radio.setTransmitSerialNumber(true)
radio.setTransmitPower(7)
serial.redirectToUSB()
basic.showIcon(IconNames.Giraffe)
basic.forever(function () {
    if (state == 1) {
        if (input.runningTime() - handshakeStartTime > 10 * 1000) {
            state = 2
            response = ""
            for (let microbitDevice of microbitDevices) {
                if (response.length > 0) {
                    response = "" + response + "," + microbitDevice
                } else {
                    response = microbitDevice
                }
            }
            serial.writeLine("enrol=" + response)
            // basic.showIcon(IconNames.Triangle)
        }
    }
})
