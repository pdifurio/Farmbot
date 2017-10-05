
#import libraries
import logging

import json

import logging.handlers

import paho.mqtt.client as mqtt

import serverSettings as settings

import serial

import RPi.GPIO as GPIO

import time

import numpy as np

import helper

# -------------------------------------------

#    Init program

# -------------------------------------------
   
g_cmd = '0'
g_absPos = '0'
def onMessage(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    messageDict = json.loads(payload)
    print('Notification received on topic ' + msg.topic + ', ' + payload)
    global g_cmd
    if msg.topic == '/FarmBot/Command/update':
        if messageDict['Update'] == 'Status':
            client.publish("/" + "FarmBot/CommandStatus", "updated status")
            g_cmd = "1"
        
    if msg.topic == '/FarmBot/Command/unalarm':
      if messageDict['Alarm'] == 'Disable':
          mqttClient.publish("/" + "FarmBot/CommandStatus", "Reset Alarm")
          g_cmd = '2'

    if msg.topic == '/FarmBot/Command/Home':
      if messageDict['Home'] == 'Home':
          mqttClient.publish("/" + "FarmBot/CommandStatus", "Return Home")
          g_cmd = '3'
          
# New Absolute X Axis
    if msg.topic == '/FarmBot/Command/Absolute':
      global g_absPos
      print(messageDict['absolute_position'])
      if messageDict['CommandType'] == 'AbsoluteMoveX':
          mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position X")
          g_absPos = messageDict['absolute_position']
          print("Next Line")
          print(g_absPos)
          g_cmd = '4'
      # Absolute Y Axis
      if messageDict['CommandType'] == 'AbsoluteMoveY':
          mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position Y")
          g_absPos = messageDict['absolute_position']
          print(g_absPos)
          g_cmd = '5'
      # Absolute Z Axis
      if messageDict['CommandType'] == 'AbsoluteMoveZ':
          mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position Z")
          g_absPos = messageDict['absolute_position']
          print(g_absPos)
          g_cmd = '6'

    if msg.topic == '/FarmBot/Command/WaterAll':
        if messageDict['WaterAll'] == 'Enable':
          client.publish("/" + "FarmBot/CommandStatus", "Begin Water All")
          g_cmd = '7'



# Create object
farmBot = helper.FarmBot()
status = helper.FarmBotStatus()
status2 = helper.FarmBotStatus()
#mqttComm = helper.MqttComm()
rPi = helper.Rpi()
sm = helper.StateMachine()

# Set up a specific logger with our desired output level
logger = logging.getLogger('serverProcessor')
farmBot.setupLogger(logger, logging)
logger.info('Logger Initialized')

#Initialize Serial Connection
ser = serial.Serial(settings.SERIAL_CLIENT, settings.SERIAL_BAUD_RATE,timeout=1)
ser2 = serial.Serial(settings.SERIAL_CLIENT_2, settings.SERIAL_BAUD_RATE, timeout=1)
logger.info('Serial Initialized')

# Initialize MQTT, connect to the broker, and start the background thread (loop) that handles MQTT events
mqttClient = mqtt.Client()

mqttClient.on_connect = helper.onConnect
mqttClient.on_message = onMessage
mqttClient.on_publish = helper.onPublish

mqttClient.connect(settings.MQTT_BROKER_IP, settings.MQTT_BROKER_PORT, 60)

mqttClient.loop_start()

logger.info('Server started')


# -------------------------------------------

#    Main program

# -------------------------------------------

while not sm.Complete:

    if sm.State != sm.PrevState:
        sm.EnteringState = True
        sm.PrevState = sm.State
    else:
        sm.EnteringState = False

    if sm.State == 0:
        # Invalid sm.State
        if sm.EnteringState:
            logger.info('FarmBot State: Invalid')

    elif sm.State == 1:
        # Initializing 
        logger.info('FarmBot State: Initializing')

        # GPIO Setup
        rPi.pinSetup(GPIO)
        
        # Mqtt setup
        topics = []
        print("\n")
        topics.append('FarmBot/Command/xAxis')
        topics.append('FarmBot/Command/yAxis')
        topics.append('FarmBot/Command/zAxis')
        topics.append('FarmBot/Command/Home')
        topics.append('FarmBot/Command/Absolute')
        topics.append('FarmBot/Command/unalarm')
        topics.append('FarmBot/Command/update')
        topics.append('FarmBot/Command/WaterAll')

        #Create Position Array
        posIndex = 0
        positions = [(28,7), (28, 18), (28, 30), (70, 30), (70, 18), (70, 7), (120, 7), (120, 18), (120, 30)]
        currentPosX = 0
        currentPosY = 0


        print('Listening on topics:')
        for i in range(len(topics)):
            mqttClient.subscribe("/" + topics[i]);
            print(topics[i])
        logger.info('FarmBot Initialized')
        time.sleep(3)
        sm.State = 2

    elif sm.State == 2:
        # Empty read buffer 
        if sm.EnteringState:
            logger.info('FarmBot State: Empty Read Buffer')

        if farmBot.commandComplete(ser) == 0:
            sm.State = 3
        else:
            print("Clearing buffer")    

    elif sm.State == 3:
        # Empty read buffer
        if sm.EnteringState:
            logger.info('FarmBot State: Empty Read Buffer')

        if farmBot.commandComplete(ser2) == 0:
            sm.State = 10
        else:
            print("Clearing buffer")

    elif sm.State == 10:
        if sm.EnteringState == True:
            logger.info('FarmBot State: Waiting for Command')
            sm.PrevState = sm.State
            g_cmd = "0"
            g_absPos = "0"
            print("\n")
            print("##############################")
            print("Select Command")
            print("##############################")
            print("Command 1: Status")
            print("Command 2: Reset Error")
            print("Command 3: Home")
            print("Command 4: Absolute X Move")
            print("Command 5: Absolute Y Move")
            print("Command 6: Absolute Z Move")
            print("Command 7: Water All")
            print("'exit' to exit program")
            print("##############################")
            print("\n")

        if settings.MANUAL_MODE: 
            g_cmd = raw_input()
        if g_cmd != "0":    
            print('received', g_cmd)
        #Status
        if g_cmd == "1":
            sm.State = 21
        elif g_cmd == "2":
            sm.State = 22 
        elif g_cmd == "3": 
            sm.State = 23
        elif g_cmd == "4":
            sm.State = 24
        elif g_cmd == "5":
            sm.State = 25
        elif g_cmd == "6":
            sm.State = 26
        elif g_cmd == "7":
            sm.State = 40
        elif g_cmd == "exit":
            sm.Complete = True
        elif g_cmd != "0":
            print("Invalid Input", g_cmd)

    elif sm.State == 21:
        # Status Update
        if sm.EnteringState == True:
            logger.info('FarmBot State: Status Update')
            ser.write('?\r') 
            print('message sent')
            sm.Done = False
            
        if not sm.Done:
            if status.ok:
                print('Command Complete')
                sm.Done = True
                sm.State = 10
            elif status.NothingToRead:
                print('Serial Failed to Read')
                sm.Done = True
                sm.State = 10
            else:
                print('Processing Command')
    
    elif sm.State == 22:
        # Reset Error
        if sm.EnteringState:
            logger.info('FarmBot State: Reset Error')
            ser.write('$X\r')
            ser2.write('$X\r')
            print('message sent')
            sm.Done = False
        if not sm.Done:
            if status.ok:
                print('Command Complete')
                sm.Done = True
                sm.State = 10
            elif status.NothingToRead:
                print('Serial Failed to Read')
                sm.Done = True
                sm.State = 10
            else:
                print('Processing Command')

    elif sm.State == 23:
        # Home FarmBot
        if sm.EnteringState:
            logger.info('FarmBot State: Homing')
            GPIO.output(19, GPIO.LOW)
            ser.write('$H\r')
            ser2.write('$H\r')
            print('message sent')
            sm.Done = False

        if not sm.Done:
            if status.ok and status2.ok:
                print('Command Complete')
                sm.Done = True
                sm.State = 10
            elif status.NothingToRead or status2.NothingToRead:
                print('Serial Failed to Read')
                sm.Done = True
                sm.State = 10
            else:
                print('Processing Command')
    
    elif sm.State == 24:
        # Absolute Move X
        if sm.EnteringState:
            logger.info('FarmBot State: Absolute Move X')
            if int(g_absPos) > 0:
                command_string = "G0 X-"+g_absPos+"Y-"+g_absPos+"\r"
                ser.write(command_string) 
                print('message sent', command_string)
                sm.Done = False
            else:
                print("Invalid Move Position")
                sm.Done = True
                
        if not sm.Done:
            if status.ok:
                print('Command Complete')
                sm.Done = True
                sm.State = 10
            elif status.NothingToRead:
                print('Serial Failed to Read')
                sm.Done = True
                sm.State = 10
            else:
                print('Processing Command')

    elif sm.State == 25:
        # Absolute Move Y
        if sm.EnteringState:
            logger.info('FarmBot State: Absolute Move Y')
            if int(g_absPos) > 0:
                command_string = "G0 Z-" + g_absPos + "\r"
                ser.write(command_string)
                print('message sent', command_string)
                sm.Done = False
            else:
                print("Invalid Move Position")
                sm.Done = True

        if not sm.Done:
            if status.ok:
                print('Command Complete')
                sm.Done = True
                sm.State = 10
            elif status.NothingToRead:
                print('Serial Failed to Read')
                sm.Done = True
                sm.State = 10
            else:
                print('Processing Command')

    elif sm.State == 26:
        # Absolute Move Z
        if sm.EnteringState:
            logger.info('FarmBot State: Absolute Move Z')
            if int(g_absPos) > 0:
                command_string = "G0 Z-" + g_absPos + "\r"
                ser2.write(command_string)
                print('message sent', command_string)
                sm.Done = False
            else:
                print("Invalid Move Position")
                sm.Done = True

        if not sm.Done:
            if status2.ok:
                print('Command Complete')
                sm.Done = True
                sm.State = 10
            elif status2.NothingToRead:
                print('Serial Failed to Read')
                sm.Done = True
                sm.State = 10
            else:
                print('Processing Command')



            
    elif sm.State == 40:
        # Water All plants
        if sm.EnteringState:
            print("40")
            posX = positions[posIndex][0]
            posY = positions[posIndex][1]
            print(posIndex,posX,posY)
            if currentPosX == posX:
                sm.State = 41
            else:
                logger.info('FarmBot State: Water All')
                ser.write('G0 X-' + str(posX) + ' Y-' + str(posX) + '\r')
                
        if status.Run:
            sm.State = 41
        else:
            print("Waiting for Move to Start")
            
    elif sm.State == 41:
        if sm.EnteringState:
            print('41')
        if status.Idle:
            sm.State = 42
            
    elif sm.State == 42:
        if sm.EnteringState:
            print('42')
            if currentPosY == posY:
                sm.State = 43
            else:
                ser.write('G0 Z-' + str(posY) + '\r')
        if status.Run:
            sm.State = 43
        else:
            print("Waiting for Move to Start")
            
    elif sm.State == 43:
        if sm.EnteringState:
            print('43')
        if status.Idle:
            sm.State = 44
        else:
            print("Moving")
            
    elif sm.State == 44:
        if sm.EnteringState:
            print('44')
            ser2.write('G0 Z-9\r')
        if status2.Run:
            sm.State = 45
        else:
            print("Waiting for Move to Start")
            
    elif sm.State == 45:
        if sm.EnteringState:
            print('45')
        if status2.Idle:
            sm.State = 46
            
    elif sm.State == 46:
        if sm.EnteringState:
            print('46')
            count = 0
            GPIO.output(19, GPIO.HIGH)
        if count >= 66:
            GPIO.output(19, GPIO.LOW)
            sm.State = 47
        else:
            count = count + 1
            
    elif sm.State == 47:
        if sm.EnteringState:
            print('47')
            ser2.write('G0 Z-6\r')
        if status2.Run:
            sm.State = 48
        else:
            print("Waiting or Move to Start")
            
    elif sm.State == 48:
        if sm.EnteringState:
            print('48')
            
        if status2.Idle:
            if posIndex == 8:
                posIndex = 0
                sm.State = 10
                currentPosX = 0
                currentPosY = 0
            else:
                currentPosX = posX
                currentPosY = posY
                posIndex = posIndex + 1
                sm.State = 40
        else:
            print("Waiting for move to complete")

    elif sm.State == 100:
        # error sm.State
        if sm.EnteringState:
            logger.warning('FarmBot State: Error')
        
    else:
        print('FarmBot in unkown sm.State')
        logger.warning('FarmBot State: Unknown')
    
    # Update Status
    farmBot.updateStatus(status, sm.State, ser, "1")
    farmBot.updateStatus(status2, sm.State, ser2, "2")
    time.sleep(.05)

# Stops and disconnects the client if Done

mqttClient.disconnect()

mqttClient.loop_stop()



logger.info('Server stopped')
    
    
    
