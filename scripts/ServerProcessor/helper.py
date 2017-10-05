'''
class FarmBotCommands(Enum):
    HOME = 10
    RESET = 20
    WATER_ALL = 30
'''
import serverSettings as settings
import json
import time

class StateMachine:
    State = 1
    PrevState = 0
    EnteringState = False
    Complete = False
    Done = False

    def __init__(self):
        self.State = 1
        self.PrevState = 0
        self.EnteringState = False
        self.Complete = False
        self.Done = False


# class MqttComm:
# class responsible for mqtt communication
def onConnect(client, userdata, rc):
    print('connected to MQTT broker with result code ' + str(rc))

    # Subscribing here means that if we lose the connection and

    # reconnect then subscriptions will be renewed.
    if rc == 0:
        client.subscribe("+/Topic1/Subtopic1", 2)


def onMessage(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    messageDict = json.loads(payload)
    print('Notification received on topic ' + msg.topic + ', ' + payload)

    # Below is the x-axis action (Arduino 1: X Axis)
    if msg.topic == '/FarmBot/Command/xAxis':
        if messageDict['xAxis'] == 'Left':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "X Axis Left")
            ser.write('$X\r')
            ser.write('G0 Z-50\r')
        if messageDict['xAxis'] == 'Right':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "X Axis Right")
            ser.write('$X\r')
            ser.write('G0 Z50\r')

    # Below is the y-axis action (Arduino 1: Y & Z Axis)
    if msg.topic == '/FarmBot/Command/yAxis':
        if messageDict['yAxis'] == 'Forward':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Y Axis Forward")
            ser.write('$X\r')
            ser.write('G0 Y150 X150\r')
        if messageDict['yAxis'] == 'Backward':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Y Axis Backward")
            ser.write('$X\r')
            ser.write('G0 Y-150 X-150\r')

    # Below is the z-axis action (Arduino 2: Z Axis)
    if msg.topic == '/FarmBot/Command/zAxis':
        if messageDict['zAxis'] == 'Up':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Z Axis Up")
            ser2.write('$X\r')
            ser2.write('G0 Z-1\r')
        if messageDict['zAxis'] == 'Down':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Z Axis Down")
            ser2.write('$X\r')
            ser2.write('G0 Z-12\r')

    if msg.topic == '/FarmBot/Command/unalarm':
        if messageDict['Alarm'] == 'Disable':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Alarm Reset")
            ser.write('$X\r')
            ser2.write('$X\r')

            # if msg.topic == '/FarmBot/Command/update':
            # Do nothing

    if msg.topic == '/FarmBot/Command/update':
        if messageDict['Update'] == 'Status':
            client.publish("/" + "FarmBot/CommandStatus", "Updated Status")
            global g_cmd
            g_cmd = "1"
            print(g_cmd)
            # Home Button (will move all axises back to zero)
            # Will update once limit switches are complete

    if msg.topic == '/FarmBot/Command/Home':
        if messageDict['Home'] == 'Home':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Return Home")
            print('Homing FarmBot')
            # Homing
            GPIO.output(19, GPIO.LOW)
            ser.write('$21 = 1\r')
            ser2.write('$21 = 1\r')
            ser.write('$22 = 1\r')
            ser2.write('$23 = 1\r')
            time.sleep(1)
            ser.write('$H\r')
            ser2.write('$H\r')

            # Absolute X Axis
    if msg.topic == '/FarmBot/Command/Absolute':
        print(messageDict['absolute_position'])
        if messageDict['CommandType'] == 'AbsoluteMoveX':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position X")
            print('G0 X' + messageDict['absolute_position'] + '\r')
            ser.write('G0 X' + messageDict['absolute_position'] + '\r')
        # Absolute Y Axis
        if messageDict['CommandType'] == 'AbsoluteMoveY':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position Y")
            print('G0 Y' + messageDict['absolute_position'] + '\r')
            ser.write('G0 Y' + messageDict['abosolute_position'] + '\r')
        # Absolute Z Axis
        if messageDict['CommandType'] == 'AbsoluteMoveZ':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position Z")
            print('G0 Z' + messageDict['absolute_position'] + '\r')
            ser2.write('G0 Z' + messageDict['abosolute_position'] + '\r')

    if msg.topic == '/FarmBot/Command/WaterAll':
        if messageDict['WaterAll'] == 'WaterAll':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "Watering All")
            print('Watering All')

    """
     # Absolute Z Axis
    if msg.topic == '/FarmBot/Command/absolute_position':
        if messageDict['moveType'] == 'absolute':
        if messageDict['moveAxis'] == 'zAxis':
            mqttClient.publish("/" + "FarmBot/CommandStatus", "At New Position")
            # ser.write('G91 G0 Z'+messageDict['moveDistance']\r')
    """


def onPublish(client, userdata, mid):
    print('message ' + str(mid) + ' published')


class Rpi:
    # Pin Definitons:
    moistureSensor = 2  # Broadcom pin 2 (P1 pin 13)
    zAxisUpSwitch = 25  # Broadcom pin 2 (P1 pin 15)
    zAxisDownSwitch = 25  # Broadcom pin 2 (P1 pin 15)
    yAxisForwardSwitch = 25  # Broadcom pin 2 (P1 pin 15)
    yAxisBackwardSwitch = 25  # Broadcom pin 2 (P1 pin 15)
    xAxisLeftSwitch = 25  # Broadcom pin 2 (P1 pin 15)
    xAxisRightSwitch = 25  # Broadcom pin 2 (P1 pin 15)

    def readSensor():
        return result

    def pinSetup(self, GPIO):
        GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
        GPIO.setwarnings(False)
        GPIO.setup(Rpi.zAxisUpSwitch, GPIO.IN)  # moisture pin set as input
        GPIO.setup(Rpi.zAxisDownSwitch, GPIO.IN)  # moisture pin set as input
        GPIO.setup(Rpi.yAxisForwardSwitch, GPIO.IN)  # moisture pin set as input
        GPIO.setup(Rpi.yAxisBackwardSwitch, GPIO.IN)  # moisture pin set as input
        GPIO.setup(Rpi.xAxisLeftSwitch, GPIO.IN)  # moisture pin set as input
        GPIO.setup(Rpi.xAxisRightSwitch, GPIO.IN)  # moisture pin set as input
        GPIO.setup(19, GPIO.OUT)
        print('GPIO Setup')


class FarmBotStatus:
    Idle = False
    Run = False
    Hold = False
    Door = False
    Home = False
    Alarm = False
    Check = False
    ok = True
    NothingToRead = False


class FarmBot:
    # class variables defined here
    initialized = False

    # command = FarmBotCommands
    def __init__(self):
        FarmBot.initialized = True
        print('FarmBot Initialized')

    def commandComplete(self, ser):
        try:
            result = ser.readline()
            print(result)
            if result == '':
                return 0

            elif result == 'ok\r\n':
                return 1
            else:
                print(result)

                # commandStatus(result)
        except:
            print('nothing to read')
            return 0

    def updateStatus(self, status, state, ser, ID):
        # update status
        if status.ok and state > 3:
            status.NothingToRead = False
            ser.write('?\r')
            status.ok = False
        try:
            result = ser.readline()
            # if result == '':
            #    print("Empty String")
            if result == 'ok\r\n':
                status.ok = True
            else:
                # print(result)
                word = result.split(",")
                if word[0] == "<Idle" and not status.Idle:
                    print("status " + ID + " changed to Idle")
                    status.Idle = True
                    status.Run = False
                    status.Hold = False
                    status.Door = False
                    status.Home = False
                    status.Alarm = False
                    status.Check = False
                elif word[0] == "<Run" and not status.Run:
                    print("status " + ID + " changed to Run")
                    status.Idle = False
                    status.Run = True
                    status.Hold = False
                    status.Door = False
                    status.Home = False
                    status.Alarm = False
                    status.Check = False
                elif word[0] == "<Hold" and not status.Hold:
                    print("status " + ID + " changed to Hold")
                    status.Idle = False
                    status.Run = False
                    status.Hold = True
                    status.Door = False
                    status.Home = False
                    status.Alarm = False
                    status.Check = False
                elif word[0] == "<Door" and not status.Door:
                    print("status " + ID + " changed to Door")
                    status.Idle = False
                    status.Run = False
                    status.Hold = False
                    status.Door = True
                    status.Home = False
                    status.Alarm = False
                    status.Check = False
                elif word[0] == "<Home" and not status.Home:
                    print("status " + ID + " changed to Home")
                    status.Idle = False
                    status.Run = False
                    status.Hold = False
                    status.Door = False
                    status.Home = True
                    status.Alarm = False
                    status.Check = False
                elif word[0] == "<Alarm" and not status.Alarm:
                    print("status " + ID + " changed to Alarm")
                    status.Idle = False
                    status.Run = False
                    status.Hold = False
                    status.Door = False
                    status.Home = False
                    status.Alarm = True
                    status.Check = False
                elif word[0] == "<Check" and not status.Check:
                    print("status " + ID + " changed to Check")
                    status.Idle = False
                    status.Run = False
                    status.Hold = False
                    status.Door = False
                    status.Home = False
                    status.Alarm = False
                    status.Check = True
                elif not word[0] == '' and not word[0] == "<Idle" and not word[0] == "<Run" and not word[
                    0] == "<Hold" and not word[0] == "<Door" and not word[0] == "<Home" and not word[
                    0] == "<Alarm" and not word[0] == "<Check":
                    print('invalid word: ', word[0])
        except:
            print('nothing to read')
            status.NothingToRead = True

    def waterAllMove(self, GPIO, ser, ser2, posX, posY):
        ser.write('G0 X-' + posX + ' Y-' + posX + '\r')
        ser.write('G0 Z-' + posY + '\r')
        ser2.write('G0 Z-12\r')
        GPIO.output(19, GPIO.HIGH)
        time.sleep(10)
        GPIO.output(19, GPIO.LOW)
        ser2.write('G0 Z-5\r')
        time.sleep(3)

    def waterAllPos(self, posX, posY):

        y = 0

    def commandStatus(result):
        print('GRBL Serial: ', result)
        try:
            parse = result.split(',')
            print(parse)
            print(parse[0])
        except:
            print('Unable to parse')

    def setupLogger(self, logger, logging):
        logger.setLevel(settings.LOG_LEVEL)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(name)s: %(message)s')
        handler = logging.handlers.RotatingFileHandler(settings.LOG_FILE_NAME,

                                                       maxBytes=settings.LOG_FILE_SIZE,

                                                       backupCount=settings.LOG_FILE_COUNT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        print('logger setup')


'''
    def waterAll():
        ser.write('$X\r')
        ser2.write('$X\r')
        #ser.write('$H\r')
        #ser2.write('$H\r')

        Step 1:
        ser.write('G0 Y-28 X-28\r')
        ser.write('G0 Z-7\r')
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        time.sleep(10)
        GPIO.output(19,GPIO.LOW)
        ser2.write('G0 Z-5\r')
        time.sleep(3)

        time.sleep(5)
        ser.write('G0 Y-28 X-28\r')
        ser.write('G0 Z-7\r')
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        GPIO.output(19,GPIO.LOW)
        ser2.write('G0 Z-5\r')
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Z-18\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Z-30\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Y-70 X-70\r')
        ser.write('G4 P4\r')
        ser2.write('G4 P4\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Z-18\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Z-7\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Y-120 X-120\r')
        ser.write('G4 P4\r')
        ser2.write('G4 P4\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Z-18\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        time.sleep(5)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        ser.write('G0 Z-30\r')
        time.sleep(5)
        ser2.write('G0 Z-12\r')
        GPIO.output(19,GPIO.HIGH)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        time.sleep(5)
        ser2.write('G0 Z-5\r')
        GPIO.output(19,GPIO.LOW)
        ser.write('G4 P3\r')
        ser2.write('G4 P3\r')
        time.sleep(5)
        print("Complete")
'''
