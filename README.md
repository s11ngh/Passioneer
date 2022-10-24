# Passioneer: Find your next passion!
 🥇 Passioneer won the **Best App - Emerging** Award at [HackGT 9](https://devpost.com/software/passioneer)! 🥇  
 

## 💡Inspiration

What if Charlie Parker had never discovered his passion for drumming. The world would never have seen the best solo ever played. Without passion. are vou living or are you merely alive?
However, "finding your passion" is much easier said than done. To start off with, there are several possible
activities one might have a latent talent for: however, trying each one out isn't feasible because of so many reasons
the main ones being a huge cost, time, and equipment barrier. Our team wanted to remove these barriers, making it
ever so easy for the general public to try whatever *they want whenever they want* 
This is the vision with which passioneer was born - helping you find your next passion

  
## 💿 What it does

Passioneer brings music and fitness to your computer while giving accurate feedback using our computer vision and machine learning models. Passioneer is also your gym trainer, yoga guru and music teacher! We are committed towards making Passioneer, so we made Passioneer voice enabled.

##  💻 How we built it

As the clock struck nine, we made our way to the drawing board, and finalized the entire project down to its core. The project was a web-based application with an easy-to-use UI. Navigating around the homepage led to four different models — each helping in a different field of activity. We knew that integrating a camera based model into a web page might have several tedious nuances to it; however, we figured our big tech brains were enough to handle a couple hours of brutally exhausting debugging. And, so, we went ahead with it anyway with the “We’ll deal with it when it faces us!” attitude.

Early on after the hacking commenced, we decided to split the work into three rough parts: Jahnavi and Sai were to handle everything related to the workings of the OpenCV models, Jeet was to handle everything related to the front-end and the webpage, and Ujjwal handled integrating the OpenCV script (Made in Python) into the WebPage using Flask.

## ⏳ Challenges we ran into

Ten hours in, although we weren’t making progress as fast as we would’ve liked, we still hadn’t hit a problem we couldn’t just StackOverflow our way out of. So, everything was a green flag for now. A couple hours of coding later, Ujjwal informed us about what became the bane of all our existences: Lag. You see, Flask is a fairly heavy python based framework; which is why when you implement an already heavy model to a webpage on a localhost, it leads to extreme lag. At one point, Ujjwal hit one of the virtual drums, and it took more than five seconds for the webcam feed to reload. Which is why we were left with no choice but to scrap using Flask as a whole and switch to a completely different framework. 
We tried substituting Flask with other python based frameworks like Django and Pyramid; however, while they solved the lag issue, they came with their own list of problems. Perplexed, we stared at a blank wall for the next twenty minutes— just thinking. Just when things started to look bleak, Jahnavi’s face cheered up like a beacon of hope peaking through a dusky, starry night. “Have you guys heard of Streamlit?” she asked. Streamlit is an open-source python based framework, and it works wonders when the task has something to do with embedding a script onto a webpage. However, since its a farly obscure technology, none of us had any experience working with it, which led all of us to learn an entirely new technology in the span of an hour.
  


## 🧠 What we learned

A few hours into development, we learned that research on CV and ML models such as pose detection discount the hundreds of problems a developer needs to overcome to actually implement them in a full stack application. When Flask did not work as intended, we learned to adapt, learn a new techstacks on the fly and move to Streamlit. Having a team with diverse skills and experiences helped us perform at our best efficiency.

## 👷‍♂️ What's next for Passioneer
We plan on adding several more hobbies for users to try out and tuning our models to support object detection in more challenging backgrounds to improve the overall function of our project. We would also try to proceed with development in making Passioneer fully accessible to people with disablities.

## Experience Passioneer
[Devpost](https://devpost.com/software/passioneer?ref_content=user-portfolio&ref_feature=in_progress)  
[Website](https://pradyumnach.github.io/Passioneers/)

## Installation
1. Install the requirements by ```conda env create -f environment.yaml```
2. Activate the environment by ```conda activate hackgt```.
3. Start the Streamlit server by ```streamlit run streamlit_app.py```. It opens a browser page, but that's not our landing page.
4. Open ```index.html```, the landing page. Heading redirects to the Streamlit server started in step 3.
