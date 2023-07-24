import serial
import time
import sqlite3
import requests
import json
import mysql.connector
import random


# emotion_list = ["sad","angry" , "happy", "pleased", "neutral"]
# emotion_list = ["sad", "neutral", "sad","angry" , "happy"]

# song_list = ["A","B","C","D","E"]

# conn = mysql.connector.connect(
#	host='192.168.137.1',
#	user='rpi',
#	port=3307,
#	password='password'
# )

def sendCommand(command):
    command = command + '\n'
    ser.write(str.encode(command))


def waitResponse():
    response = ser.readline()
    response = response.decode('utf-8').strip()

    return response


def saveData(temperatures):
    c = conn.cursor()

    for temperature in temperatures:
        data = temperature.split('=')

        sql = "INSERT INTO temperature (devicename, temp, timestamp) VALUES('" + data[0] + "', " + data[
            1] + ", datetime('now', 'localtime'))"
        c.execute(sql)

    conn.commit()

    temperatures.clear()


try:

    print("Listening on /dev/ttyACM0... Press CTRL+C to exit")
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)

    # conn = sqlite3.connect('temperature.db')

    # Handshaking
    sendCommand('handshake')

    strMicrobitDevices = ''

    while strMicrobitDevices == None or len(strMicrobitDevices) <= 0:
        strMicrobitDevices = waitResponse()
        time.sleep(0.1)

    strMicrobitDevices = strMicrobitDevices.split('=')

    # print(len(strMicrobitDevices[1]))
    if len(strMicrobitDevices[1]) > 0:

        listMicrobitDevices = strMicrobitDevices[1].split(',')
        # print(len(listMicrobitDevices))

        if len(listMicrobitDevices) > 0:

            for mb in listMicrobitDevices:
                print('Connected to micro:bit device {}...'.format(mb))

            # i = 0
            time.sleep(5)
            while True:

                wrl = open('/home/group6/label.txt', 'r')
                label = wrl.read()
                wrn = open('/home/group6/name.txt', 'r')
                name = wrn.read()
                # label = 'sad'
                # name = "ZRC"
                song = ""

                if name != "Unk":
                    # breakpoint()
                    print('Sending command to all micro:bit devices...')
                    # print(name)
                    base_url = "http://192.168.137.1:5000/api/mood"
                    put_url = base_url + "/normal"
                    moodState = {"name": name, "mood": label}
                    # print(moodState)
                    headers = {"content_type": "application/json"}
                    response = requests.put(put_url, headers=headers, data=json.dumps(moodState))
                    song_url = base_url + "/song?name=" + name
                    response = requests.get(song_url)
                    song = json.loads(response.content)
                    print('Song: ', end='')
                    print(song)

                    # commandToTx = 'mood=' +	label
                    commandToTx = 'mood=' + label
                    commandSong = ',song=' + song[0]
                    print('connand: ')
                    print('cmd:' + commandToTx + commandSong)

                    sendCommand('cmd:' + commandToTx + commandSong)
                    # i = i+1
                    print('Finished sending command to all micro:bit devices...')
                time.sleep(5)
                '''if commandToTx.startswith('mood='):

                    strSensorValues = ''

                    while strSensorValues == None or len(strSensorValues) <= 0:

                        strSensorValues = waitResponse()
                        time.sleep(0.1)

                if __name__ == "__main__":
    listSensorValues = strSensorValues.split(',')

                    for sensorValue in listSensorValues:

                        print(sensorValue)

                    saveData(listSensorValues)'''

except KeyboardInterrupt:

    print("Program terminated!")

except Exception as e:

    print('********** UNKNOWN ERROR')
    print(e)

finally:
    if ser.is_open:
        ser.close()

    conn.close()

