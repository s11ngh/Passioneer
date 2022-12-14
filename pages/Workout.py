import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

import streamlit as st




def main_loop():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = " "

    st.title("Pushup Counter")
    imageLocation = st.empty()
    countLocation = st.empty()

    while cap.isOpened():
        ret, img = cap.read() 
        
        width  = cap.get(3)  
        height = cap.get(4)  
        
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23,25)
            
            
            per = np.interp(elbow, (90, 160), (0, 100))
            
            #Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            
            if elbow > 160 and shoulder > 40 and hip > 160:
                form = 1
            # else:
            #     form = 0
        
            #Check for full range of motion for the pushup
            if form == 1:
                if per == 0:
                    if elbow <= 90 and hip > 160:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = " "
                        
                if per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = " "
                            
                    
                        
        
            # print(count)
            
            #Draw Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)


            #Pushup counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
            
            #Feedback 
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)

            
        imageLocation.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        countLocation.text(f"Count: {count}")
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()