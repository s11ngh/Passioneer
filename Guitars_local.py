import cv2
import numpy as np
import time
import pygame
# import streamlit as st

GRAD_THRESH = 5  # gradient threshold
CLS_THRESH = 0.2  # classification threshold

class Chord:
    def __init__(self, y=None):
        self.y = y
        self.lastDet = None
    
    def checkStrum(self, coords):
        if self.lastDet is not None and time.time() - self.lastDet < 0.5:
            return False
        if abs(coords[1] - self.y) < 0.025:
            self.lastDet = time.time()
            return True

# chord_A = Chord(0.275)
# chord_B = Chord(0.425)
# chord_C = Chord(0.575)
# chord_D = Chord(0.725)

chord_A = Chord(168/400)
chord_B = Chord(196/400)
chord_C = Chord(224/400)
chord_D = Chord(253/400)

pygame.mixer.init()
sounds = [
    ['./sounds/e1.mp3','./sounds/e2.mp3','./sounds/e3.mp3','./sounds/e4.mp3'],
    ['./sounds/a1.mp3','./sounds/a2.mp3','./sounds/a3.mp3','./sounds/a4.mp3'],
    ['./sounds/d1.mp3','./sounds/d2.mp3','./sounds/d3.mp3','./sounds/d4.mp3'],
    ['./sounds/g1.mp3','./sounds/g2.mp3','./sounds/g3.mp3','./sounds/g4.mp3'],
]
sounds = [[pygame.mixer.Sound(x) for x in chord] for chord in sounds]

def getGuitarImage(file):
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # h, w, _ = image.shape
    # image = cv2.line(image, (0, int(chord_A.y * h)), (w-1, int(chord_A.y * h)), (0, 0, 0, 255), 5)
    # image = cv2.line(image, (0, int(chord_B.y * h)), (w-1, int(chord_B.y * h)), (0, 0, 0, 255), 5)
    # image = cv2.line(image, (0, int(chord_C.y * h)), (w-1, int(chord_C.y * h)), (0, 0, 0, 255), 5)
    # image = cv2.line(image, (0, int(chord_D.y * h)), (w-1, int(chord_D.y * h)), (0, 0, 0, 255), 5)
    return image

def coordOverlay(frame, is_marker, coords, pick=None):

    H, W, _ = frame.shape
    color = (255,0,255)

    if not is_marker:
        return frame[:, ::-1, :]
    # coords = (100, 300)
    coords = int(coords[0]*W), int(coords[1]*H)
    if pick is None:
        radius = 10
        frame = cv2.circle(frame, coords, radius, color, -1)
    else:
        # preferred size at original res: 32, 32 (original res: 400, 750)
        pick_w, pick_h = int(32/750*W), int(32/400*H)
        pick = cv2.resize(pick, (pick_w, pick_h))
        if coords[1]-pick_h < 0 or coords[0]-pick_w//2 < 0 or coords[0]+pick_w-pick_w//2 >= W:
            return frame[:, ::-1, :]
        frame[coords[1]-pick_h: coords[1], coords[0]-pick_w//2 : coords[0]+pick_w-pick_w//2] = cv2.addWeighted(
            frame[coords[1]-pick_h: coords[1], coords[0]-pick_w//2 : coords[0]+pick_w-pick_w//2], 1,
            pick, 10, 0)

    return frame[:, ::-1, :]

def detectAndLocateMarker(frame):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # thresholded_frame1 = cv2.inRange(frame_hsv, (0, 70, 50), (10, 255, 255))
    # thresholded_frame = cv2.inRange(frame_hsv, (170, 70, 50), (180, 255, 255))
    thresholded_frame = cv2.inRange(frame_hsv, (40, 150, 80), (255, 255, 255))  #b1
    # thresholded_frame = np.logical_or(thresholded_frame1, thresholded_frame2).astype(np.uint8)

    # thresholded_frame = cv2.inRange(frame_hsv, (0, 70, 50), (10, 255, 255))
    # print(np.sum(thresholded_frame))
    thresholded_frame *= 255

    M = cv2.moments(thresholded_frame)
    if not M["m00"]:
        return False, -1, -1
    X = int(M["m10"] // M["m00"])
    Y = int(M["m01"] // M["m00"])

    h, w, _ = frame.shape
    return True, X/w, Y/h

def identifyChords(coords):
    checks = (
        chord_A.checkStrum(coords),
        chord_B.checkStrum(coords),
        chord_C.checkStrum(coords),
        chord_D.checkStrum(coords),
    )
    try:
        return checks.index(True)
    except Exception:
        return -1

def getFret():
    key = cv2.waitKey(50)
    checks = (
    key & 0xFF == ord('a'),
    key & 0xFF == ord('s'),
    key & 0xFF == ord('d'),
    # key & 0xFF == ord('f')
    )
    try:
        return checks.index(True) + 1
    except Exception:
        return 0
    
# def getFret():
#     # checks = (
#     #     keyboard.is_pressed('a'),
#     #     keyboard.is_pressed('s'),
#     #     keyboard.is_pressed('d')
#     # )
#     # checks
#     # try:
#     #     return checks.index(True) + 1
#     # except Exception:
#     #     return 0
#     print("getFret receving keyboard input:", pygame.key.get_focused())
#     if pygame.key.get_pressed()[pygame.key.key_code("a")]:
#         return 1
#     if pygame.key.get_pressed()[pygame.key.key_code("s")]:
#         return 2
#     if pygame.key.get_pressed()[pygame.key.key_code("d")]:
#         return 3
#     return -1

# def getFret(buttons):
#     try:
#         val = buttons.index(True) + 1
#         print("Fret:", val)
#         return val
#     except Exception:
#         return 0

# def init_buttons():


def playSound(chord, fret):
    # sounds[chord][fret].play()
    print("Playing chord:", chord, "fret:", fret)
    sounds[chord][fret].play()

# def init_buttons(cols):
#     buttons = []
#     for i, col in enumerate(cols):
#         with col:
#             buttons.append(st.button("Fret %d" %(i+1)))
#     # buttons.append(st.button("Fret 2"))
#     # buttons.append(st.button("Fret 3"))
#     return buttons

def main_loop():

    # pygame.init()

    cam = cv2.VideoCapture(0)
    _,  frame = cam.read()
    h, w, _ = frame.shape
    guitar_img = getGuitarImage('./images/uk_crop2.png')
    pick_img = cv2.imread('./images/pick_transparent.png', cv2.IMREAD_UNCHANGED)

    # st.title("Drums")
    # st.subheader("This app allows you to play Drums!")
    # st.text("We use OpenCV and Streamlit for this demo")
    # imageLocation = st.empty()

    # cols = st.columns([1,1,1])
    # buttons = init_buttons(cols)

    while True:
        _, frame = cam.read()
        if frame is None:
            break
        is_marker, *marker_coords = detectAndLocateMarker(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

        h, w, _ = frame.shape
        resize_h = h * 750 // w
        frame = cv2.resize(frame, (750, resize_h))
        frame[int(0.5*resize_h-400//2):400+int(0.5*resize_h-400//2), :] = \
        np.clip(0.5 * frame[int(0.5*resize_h-400//2):400+int(0.5*resize_h-400//2), :] + 0.66 * guitar_img, 0, 255).astype(np.uint8)
        
        cv2.imshow('frame', coordOverlay(frame, is_marker, marker_coords, pick_img))

        if is_marker:
            chords = identifyChords(marker_coords)
            if chords != -1:
                fret = getFret()
                playSound(chords, fret)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

if __name__ == '__main__':
    print("main_loop")
    main_loop()