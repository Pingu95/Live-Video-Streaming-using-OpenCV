import socket
import sys
import numpy as np
import cv2 as cv


addr = ("192.168.0.107", 65534) # IP Address of Receiver is input

# addr = ("127.0.0.1", 65534)
buf = 512
width = 640
height = 480
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


def send_frames():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            s.sendto(code, addr)
            data = frame.tostring()
            for i in range(0, len(data), buf):
                s.sendto(data[i:i+buf], addr)
            cv.imshow('send', frame)                # to verify webcam operation on sending end
            if(cv.waitKey(1) & 0xFF==32):
                while True:
                    if(cv.waitKey(1) & 0xFF==32):
                        break
                    if(cv.waitKey(1) & 0xFF==ord('q')):
                        s.close()
                        cap.release()
                        cv.destroyAllWindows()
                        sys.exit(0)
                       
            if(cv.waitKey(1) & 0xFF == ord('q')):    # Press Q to exit
                s.close()
                cap.release()
                cv.destroyAllWindows()
                sys.exit(0)
        else:
            break

while True:
    send_frames()
