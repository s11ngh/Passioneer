import streamlit as st
import numpy as np
import math,pickle
from PIL import Image
import cv2
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


load_model=pickle.load(open('./assets/Poses.pkl','rb'))
 
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return round(ang + 360 if ang < 0 else ang)
 
def feature_list(poseLandmarks,posename):
    return [getAngle(poseLandmarks[16],poseLandmarks[14],poseLandmarks[12]),
    getAngle(poseLandmarks[14],poseLandmarks[12],poseLandmarks[24]),
    getAngle(poseLandmarks[13],poseLandmarks[11],poseLandmarks[23]),
    getAngle(poseLandmarks[15],poseLandmarks[13],poseLandmarks[11]),
    getAngle(poseLandmarks[12],poseLandmarks[24],poseLandmarks[26]),
    getAngle(poseLandmarks[11],poseLandmarks[23],poseLandmarks[25]),
    getAngle(poseLandmarks[24],poseLandmarks[26],poseLandmarks[28]),
    getAngle(poseLandmarks[23],poseLandmarks[25],poseLandmarks[27]),
    getAngle(poseLandmarks[26],poseLandmarks[28],poseLandmarks[32]),
    getAngle(poseLandmarks[25],poseLandmarks[27],poseLandmarks[31]),
    getAngle(poseLandmarks[0],poseLandmarks[12],poseLandmarks[11]),
    getAngle(poseLandmarks[0],poseLandmarks[11],poseLandmarks[12]),
    posename]   




st.set_page_config(layout="wide")

#sidebar
st.sidebar.title('YOGA TRAINER')

mode=st.sidebar.selectbox('POSE',['Tree','Warrior'])


 

if mode=='Tree':
     
    col1, col2 = st.columns([2,3])
    with col1:
        with st.container():
            original_title = '<p style="font-family:Poppins, sans-serif; color:Black; font-size: 20px;">Tree Pose</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            gt_img=Image.open('./images/tree.jpg')
              
            gt_image = gt_img.rotate(270)
            st.image(gt_image)

    with col2:

        original_title = '<p style="font-family:Poppins, sans-serif; color:Black; font-size: 20px;">Copy the pose shown in the picture</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        
        # st.write("Copy the Pose shown in the picture")
        
        button=st.empty()
        start=button.button('Start')
        if start:
            stop=button.button('Stop')
            no_text = st.empty()
            FRAME_WINDOW = st.image([])
            accuracytxtbox = st.empty()
            accuracy_text_format = '<p style="font-family:Poppins, sans-serif; color:Black; font-size: 16px;">%s</p>'
            cap = cv2.VideoCapture(0)
            
            
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

                while cap.isOpened():
                    ret, frame = cap.read()
                    h,w,c=frame.shape 
                    
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                
                    
                    results = pose.process(image)
                    
                    
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                            )               
                    
                    FRAME_WINDOW.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    poseLandmarks=[]
                    if results.pose_landmarks:
                        for lm in results.pose_landmarks.landmark:            
                            poseLandmarks.append((int(lm.x*w),int(lm.y*h)))
                    if len(poseLandmarks)==0:
                        no_text.text("No one in Frame")
                        accuracytxtbox.text('')
                        continue
                    else:
                        no_text.text("")
                        
                        d=feature_list(poseLandmarks,1)
                        
                        rt_accuracy=int(round(load_model.predict(np.array(d).reshape(1, -1))[0],0))
                        rt_accuracy = int((rt_accuracy - 50) * 2)

                        if rt_accuracy<40:
                            accuracytxtbox.markdown(accuracy_text_format %(f"Not quite right {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=40 and rt_accuracy<60:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Good {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=60 and rt_accuracy<80:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Very Good {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=80 and rt_accuracy<100:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Almost Perfect {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=100:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Perfect"), unsafe_allow_html=True)
                        
                     
                    if stop:
                        cap.release()
                        cv2.destroyAllWindows()
                else:
                    st.write('Allow Camera Acess')
                  

         
elif mode=='Warrior':
     
    col1, col2 = st.columns([2,3])
    with col1:
        with st.container():
            original_title = '<p style="font-family:Poppins, sans-serif; color:Black; font-size: 20px;">Warrior Pose</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            gt_image = Image.open('./images/warrior.jpg')
            st.image(gt_image)
    with col2:
        original_title = '<p style="font-family:Poppins, sans-serif; color:Black; font-size: 20px;">Copy the pose shown in the picture</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        
        button=st.empty()
        start=button.button('Start')
        if start:
            stop=button.button('Stop')
            no_text = st.empty()
            FRAME_WINDOW = st.image([])
            accuracytxtbox = st.empty()
            accuracy_text_format = '<p style="font-family:Poppins, sans-serif; color:Black; font-size: 16px;">%s</p>'
            cap = cv2.VideoCapture(0)
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                while cap.isOpened():
                    ret, frame = cap.read()
                    h,w,c=frame.shape 
                    
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                
                    
                    results = pose.process(image)
                    
                    
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                            )               
                    
                    FRAME_WINDOW.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)[:,::-1,:])
                    poseLandmarks=[]
                    if results.pose_landmarks:
                        for lm in results.pose_landmarks.landmark:            
                            poseLandmarks.append((int(lm.x*w),int(lm.y*h)))
                    if len(poseLandmarks)==0:
                        no_text.text("Body Not Visible")
                        accuracytxtbox.text('')
                        continue
                    else:
                        no_text.text("")
                        
                        d=feature_list(poseLandmarks,3)
                        rt_accuracy=int(round(load_model.predict(np.array(d).reshape(1, -1))[0],0))
                        rt_accuracy = int((rt_accuracy - 50) * 2)
                        
                        if rt_accuracy<40:
                            accuracytxtbox.markdown(accuracy_text_format %(f"Not quite right {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=40 and rt_accuracy<60:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Good {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=60 and rt_accuracy<80:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Very Good {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=80 and rt_accuracy<100:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Almost Perfect {rt_accuracy}"), unsafe_allow_html=True)
                        elif rt_accuracy>=100:
                            accuracytxtbox.markdown(accuracy_text_format % (f"Perfect"), unsafe_allow_html=True)
                        
                     
                    if stop:
                        cap.release()
                        cv2.destroyAllWindows()
                else:
                    st.write('Allow Camera Access')
         

    