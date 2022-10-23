1. Install the requirements by ```conda env create -f environment.yaml```
2. Activate the environment by ```conda activate hackgt```.
3. Start the Streamlit server by ```streamlit run streamlit_app.py```. It opens a browser page, but that's not our landing page.
4. Open ```index.html```, the landing page. Heading redirects to the Streamlit server started in step 3.

## 💡Inspiration



Without passion, are you living or merely alive? There are millions of possible activities that have the potential to turn into passion. However, trying each out isn’t feasible because of cost, time, accessibility, and equipment barriers.

  

Our team wanted to remove these barriers. So we built *Passioneer*, which removes cost and accessibility barriers from these activities, and provides an on-demand experience to our users regardless of their device’s horsepower (thanks Google Cloud!).

  

## 💿 What it does

Passioneer brings music and fitness to your computer while giving accurate feedback using our computer vision and machine learning models. Passioneer is also your gym trainer, yoga guru and music teacher! We are committed towards making Passioneer, so we made Passioneer voice enabled.
##  💻 How we built it

We got ourselves a whiteboard and created an architecture for the project. We decided to create a web-based app that would act as a container for our 4 models. The models were a product of OpenCV, mediapipe, and TensorFlow. Due to the demanding nature of our model, we had to do the heavy lifting on the cloud. This ensured, Passioneer worked efficiently on *every* device.

  

After hours of debugging, fine-tuning our models, and switching frameworks, we decided to host our website on Google Cloud.

  

Assigning tasks made our workflow much smoother.: Jahnavi and Sai handled everything related to the workings of the OpenCV models while Jeet worked on the front end. Ujjwal handled integrating our model into the webpage and got the Flask server running.

## ⏳ Challenges we ran into



  

To achieve our goal of making the web app run efficiently on anything from a Chromebook to a gaming laptop we used Flask to run our server. When Ujjwal tested the virtual drums, we saw a 3-5 second lag in the camera feed. So we had to move from Flask to Streamlit to wrap up our Python app.

  

Our second issue was  finding the perfect color for detection, and tuning our model to work in different backgrounds and lighting conditions. We ended up finding success with blue objects, which is the color of our supported drumsticks and guitar plectrum.

  


## 🧠 What we learned

A few hours into development, we learned that research and whiteboard planning discount the hundreds of problems waiting for us. When Flask did not work as intended, we learned to adapt and move to Streamlit. Having a team with diverse skills and experiences helped us perform at our best efficiency.

## 👷‍♂️ What's next for Passioneer
We plan on tuning our models to support object detection in more challenging backgrounds to improve the overall function of our project. We would love to proceed with development in making Passioneer fully accessible to people with disablities.

## Experience Passioneer
[Github](https://github.com/s11ngh/Passioneer)
[enter link description here](ourwebsitelink)