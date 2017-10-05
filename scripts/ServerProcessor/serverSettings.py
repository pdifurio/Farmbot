import logging



#MQTT_BROKER_IP = 'iot.eclipse.org'

MQTT_BROKER_IP = 'localhost'

MQTT_BROKER_PORT = 1883

SERIAL_CLIENT = '/dev/ttyACM0'

SERIAL_CLIENT_2 = '/dev/ttyACM1'

SERIAL_BAUD_RATE = '115200'


MONGODB_SERVER_IP = 'localhost'

MONGODB_SERVER_PORT = 27017



LOG_FILE_NAME = 'logs/logFile.out'

LOG_FILE_SIZE = 2000000

LOG_FILE_COUNT = 10

LOG_LEVEL = logging.DEBUG
# Control Mode: True - Manual, False - Auto
MANUAL_MODE = False

VAR_COMMAND = 0
