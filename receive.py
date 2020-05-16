import socket
import sys
import numpy as np
import cv2 as cv

addr = ("192.168.0.108", 65534) # IP Address of Receiver is input

buf = 512
width = 640
height = 480
code = b'start'
num_of_chunks = width * height * 3 / buf
cv.namedWindow('recv')

def recv_frames():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk, _ = s.recvfrom(buf)
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)

        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(height, width, 3)

        cv.imshow('recv', frame)
        if(cv.waitKey(1) & 0xFF == 32):
            print("Video receiving is PAUSED")
            while True:
                if(cv.waitKey(1) & 0xFF==32):
                    print("Video receiving has RESUMED")
                    break
                if(cv.waitKey(1) & 0xFF==ord('q')):
                    print("Video receiving has ended")
                    s.close()
                    cv.destroyAllWindows()
                    sys.exit(0)
        if(cv.waitKey(1) & 0xFF==ord('q')):
            print("Video receiving has ended")
            s.close()
            cv.destroyAllWindows()
            sys.exit(0)

while True:
    recv_frames()
