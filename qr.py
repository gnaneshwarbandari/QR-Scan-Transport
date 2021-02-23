import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import wiotp.sdk.device
import random
import time
myConfig = { 
    "identity": {
        "orgId": "hj5fmy",
        "typeId": "NodeMCU",
        "deviceId": "12345"
    },
    "auth": {
        "token": "12345678"
    }
}
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
print(client)
#client.commandCallback = myCommandCallback
# Connect
client.connect()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        #print("Data", obj.data)
        a=obj.data.decode('UTF-8')
        cv2.putText(frame, a, (50, 50), font, 2,
                    (255, 0, 0), 3)
        print(a)
        myData={'data':a}
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        time.sleep(2)
        print("Published successfully", myData)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
client.disconnect()