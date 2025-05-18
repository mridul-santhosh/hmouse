import cv2
import mediapipe as mp
import numpy as np
import time
import multiprocessing
from mouse import btfpy
from g_helper import bgr2rgb
from combined_helper import pipelineOptimized
from feb_15.full.mraaz.sensor_lib import Sensors
from zero_hid import Mouse
import os
import signal

SUSPEND_TIMEOUT = 5 * 60  # 5 minutes

active_process = "ble"
interrupt = None
mp_face_mesh = mp.solutions.face_mesh
reportindex = -1
node = 0
sensor = None
usb_mouse = None
min_th = 10
m = None
motion_timer = 0

def lecallback(clientnode,op,cticn):
  global sensor
  global min_th
  x = int(shared_data.get('x',0))
  y = int(shared_data.get('y',0))
  btn = int(shared_data.get('btn',0))
  if(op == btfpy.LE_CONNECT): 
    print("Connected OK. Arrow keys move cursor. ESC stops server") 
  if(op == btfpy.LE_DISCONNECT):
      print("Disconnected from the client....")
      shared_data['disconnect'] = True
      return(btfpy.SERVER_EXIT)
  if(op == btfpy.LE_TIMER):
    send_key(x,y,btn)    
    if (time.time() - shared_data.get('time', None) > 1):
        shared_data['time'] = time.time()
        light_level = sensor.readLightLevel()
        pir_status = sensor.readPir()
        print(f"Light Level: {light_level}  lux, pir status {pir_status}")
        if (light_level < min_th):
            sensor.writeIr(1)
        else:
            sensor.writeIr(0)
  return(btfpy.SERVER_CONTINUE)

def usb_server():
    global usb_mouse
    global motion_timer
    print("USB Server Started")
    x = int(shared_data.get('x',0))
    y = int(shared_data.get('y',0))
    btn = int(shared_data.get('btn',0))
    ux = x + 256 if x < 0 else x
    uy = y + 256 if y < 0 else y
    usb_mouse.raw(btn, int(ux), int(uy), 0, 0)
    if (time.time() - shared_data.get('time', None) > 1):
        shared_data['time'] = time.time()
        light_level = sensor.readLightLevel()
        pir_status = sensor.readPir()
        print(f"Light Level: {light_level}  lux, pir status {pir_status}")
        if (light_level < min_th):
            sensor.writeIr(1)
        else:
            sensor. (0)
        if pir_status:
            print("Motion Detected")
            motion_timer = time.time()
        if time.time() - motion_timer > SUSPEND_TIMEOUT:
            print("Suspend Mode")
            os.system("systemctl suspend")

def send_key(x, y, but):
    """Send mouse movement and button press reports."""
    node = shared_data['node']
    reportindex = shared_data['reportindex']
    
    ux = x + 256 if x < 0 else x
    uy = y + 256 if y < 0 else y
    # print(f"Sending: {but}, {ux}, {uy} report index : {shared_data.get('reportindex')} node : {shared_data.get('node')}")
    btfpy.Write_ctic(node, reportindex, [but, ux, uy], 0)
    if but != 0:
        btfpy.Write_ctic(node, reportindex, [0, 0, 0], 0)

def ble_server():
    """BLE Mouse Server Process."""
    reportmap = [0x05,0x01,0x09,0x02,0xA1,0x01,0x85,0x01,0x09,0x01,0xA1,0x00,0x05,0x09,0x19,0x01,\
                0x29,0x03,0x15,0x00,0x25,0x01,0x95,0x03,0x75,0x01,0x81,0x02,0x95,0x01,0x75,0x05,\
                0x81,0x01,0x05,0x01,0x09,0x30,0x09,0x31,0x15,0x81,0x25,0x7F,0x75,0x08,0x95,0x02,\
                0x81,0x06,0xC0,0xC0]

    # NOTE the size of report (3 in this case) must appear in keyboard.txt as follows:
    #   LECHAR=Report1         SIZE=3  Permit=92  UUID=2A4D  
    report = [0,0,0]

    name = "H Mouse"
    appear = [0xC2,0x03]  # 03C2 = mouse icon appears on connecting device 
    pnpinfo = [0x02,0x6B,0x1D,0x46,0x02,0x37,0x05]
    protocolmode = [0x01]
    hidinfo = [0x01,0x11,0x00,0x02]

    if btfpy.Init_blue("mouse/mouse.txt") == 0:
        exit(0)
    
    if(btfpy.Localnode() != 1):
        print("ERROR - Edit mouse.txt to set ADDRESS = " + btfpy.Device_address(btfpy.Localnode()))
        exit(0)
        
    node = btfpy.Localnode()    

    # look up Report1 index
    uuid = [0x2A,0x4D]
    reportindex = btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid)
    if(reportindex < 0):
        print("Failed to find Report characteristic")
        exit(0)
    shared_data["node"] = node
    shared_data["reportindex"] = reportindex

    # Write data to local characteristics  node=local node
    uuid = [0x2A,0x00]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),name,0) 

    uuid = [0x2A,0x01]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),appear,0) 

    uuid = [0x2A,0x4E]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),protocolmode,0)

    uuid = [0x2A,0x4A]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),hidinfo,0)

    uuid = [0x2A,0x4B]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),reportmap,0)

    uuid = [0x2A,0x4D]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),report,0)

    uuid = [0x2A,0x50]
    btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),pnpinfo,0)
                                
    # Set unchanging random address by hard-coding a fixed value.
    # If connection produces an "Attempting Classic connection"
    # error then choose a different address.
    # If set_le_random_address() is not called, the system will set a
    # new and different random address every time this code is run.  
    
    # Choose the following 6 numbers
    # 2 hi bits of first number must be 1
    randadd = [0xD3,0x56,0xD3,0x15,0x32,0xA0]
    btfpy.Set_le_random_address(randadd)
        
    btfpy.Set_le_wait(20000)  # Allow 20 seconds for connection to complete
                                            
    btfpy.Le_pair(btfpy.Localnode(),btfpy.JUST_WORKS,0)  # Easiest option, but if client requires
                                                        # passkey security - remove this command  

    btfpy.Le_server(lecallback,10)
    
    btfpy.Close_all()

def face_tracking(shared_data):
    """Face tracking using Mediapipe with improved drag handling."""
    cap = cv2.VideoCapture(0)
    eyes_closed_start = None
    eyes_closed_threshold = 0.5

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, 
                               min_detection_confidence=0.5, 
                               min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            results = face_mesh.process(bgr2rgb(image))
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    x, y, _, r_eyes_state, l_eyes_state, mouth_state = pipelineOptimized(image, face_landmarks)
                    btn = 0

                    # Improved drag handling
                    if mouth_state == "opened":
                        btn = 1  # Keep button pressed while mouth is open
                    elif mouth_state == "closed":
                        btn = 0

                    # Right click handling remains the same
                    if r_eyes_state == "closed" and l_eyes_state == "closed":
                        if eyes_closed_start is None:
                            eyes_closed_start = time.time()
                        elif time.time() - eyes_closed_start >= eyes_closed_threshold:
                            btn = 2  # Right-click equivalent
                            eyes_closed_start = None
                    else:
                        eyes_closed_start = None

                    # Update shared data
                    shared_data['x'] = x
                    shared_data['y'] = y
                    shared_data['btn'] = btn

            cv2.imshow('Head Pose Detection',image)
            if cv2.waitKey(1) == ord('q') or shared_data.get('disconnect', False):
                break
    
    cap.release()
    cv2.destroyAllWindows()

def switch_process(args):
    global active_process, ble_process, usb_process

    if active_process == "ble":
        print("Switching to USB Process...")
        if ble_process.is_alive():
            ble_process.terminate()
            ble_process.join()
        usb_process = multiprocessing.Process(target=usb_server)
        usb_process.start()
        active_process = "usb"

    else:
        print("Switching to BLE Process...")
        if usb_process.is_alive():
            usb_process.terminate()
            usb_process.join()
        ble_process = multiprocessing.Process(target=ble_server)
        ble_process.start()
        active_process = "ble"

# Keep the script running
def exit_handler(signal, frame):
    print("Exiting...")
    interrupt.isrExit()
    exit(0)

signal.signal(signal.SIGINT, exit_handler)
if __name__ == "__main__":

    manager = multiprocessing.Manager()
    shared_data = manager.dict()
    shared_data['node'] = None
    shared_data['reportindex'] = None
    shared_data['x'] = 0
    shared_data['y'] = 0
    shared_data['btn'] = 0
    shared_data['disconnect'] = False 
    shared_data['time'] = None  
    shared_data['time'] = time.time()  
    usb_mouse = Mouse()
    sensor = Sensors(debug=True)  
    sensor.begin(Sensors.CONTINUOUS_HIGH_RES_MODE)
    interrupt = Sensors.getInterrupt()
    interrupt.isr(switch_process, None)
    ble_process = multiprocessing.Process(target=ble_server)
    usb_process = multiprocessing.Process(target=usb_server)

    face_process = multiprocessing.Process(target=face_tracking, args=(shared_data,))
    face_process.start()
    time.sleep(5)
    ble_process.start()

    
    ble_process.join()
    face_process.join()
    signal.signal(signal.SIGINT, exit_handler)
        