
import numpy as np
import time
import cv2
from pygame import mixer
import streamlit as st


class Instrument:
    def __init__(self, x, y, w, h, sound_file=None, image_file=None):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.last_played = None
        self.sound = mixer.Sound(sound_file)

        global H, W
        image = cv2.imread(image_file)
        image = cv2.resize(image, (int(w*W), int(h*H)))
        self.image = image

    def detectInRange(self, frame):
        # Converting to HSV
        frame = np.copy(frame[self.y:int(self.y+self.h*H), self.x:int(self.x+self.w*W)])
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Creating mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        
        # Calculating the number of green pixels
        sense = np.sum(mask)
        
        # Call the function to play the drum beat
        self.play_beat(sense)

        return mask

    def play_beat(self, sense):
        if sense > self.w * self.h * 0.8:
            if self.last_played is None or time.time() - self.last_played > 0.6:
                self.sound.play()
                self.last_played = time.time()

    def overlay_image(self, frame):
        global H, W
        frame[self.y:self.y+int(self.h*H), self.x:int(self.x+self.w*W)] = cv2.addWeighted(self.image, 1, frame[self.y:int(self.y+self.h*H), self.x:int(self.x+self.w*W)], 1, 0)
        return frame

def main_loop():
    mixer.init()
    # Set HSV range for detecting blue color 
    global greenLower, greenUpper
    greenLower = (40, 150, 80)
    greenUpper = (255, 255, 255)
    # thresholded_frame = cv2.inRange(frame_hsv, (40, 150, 80), (255, 255, 255))  #b1


    # Obtain input from the webcam 
    camera = cv2.VideoCapture(0)
    ret,frame = camera.read()
    global H, W
    H,W = frame.shape[:2]
    hat = Instrument(W*3//10, H*1//2, 0.2, 0.25, './sounds/high_hat_1.ogg', './images/high_hat.png')
    snare = Instrument(W*5//10, H*1//2, 0.2, 0.25, './sounds/snare_1.wav', './images/snare_drum.png')
    tom = Instrument(W*3//10, H*3//4, 0.2, 0.25, './sounds/Tom.wav', './images/Tom.png')
    bass = Instrument(W*5//10, H*3//4, 0.2, 0.25, './sounds/bass.wav', './images/bass.png')

    st.title("Drums")
    st.subheader("This app allows you to play Drums!")
    st.text("We use OpenCV and Streamlit for this demo")
    imageLocation = st.empty()

    while True:
        
        # Select the current frame
        ret, frame = camera.read()
        frame = cv2.flip(frame,1)

        if not(ret):
            break    
        
        mask = hat.detectInRange(frame)
        mask = snare.detectInRange(frame)
        mask = bass.detectInRange(frame)
        mask = tom.detectInRange(frame)
        
        frame = hat.overlay_image(frame)
        frame = snare.overlay_image(frame)
        frame = bass.overlay_image(frame)
        frame = tom.overlay_image(frame)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        imageLocation.image(frame)
        key = cv2.waitKey(1) & 0xFF
        # 'Q' to exit
        if key == ord("q"):
            break
 
    # Clean up the open windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()