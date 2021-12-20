# Capstone-Design-2-Graduation-Project-from-Dongguk-University-

## Topic: Tracking AI-based colon polyps patients' eating habits and providing solutions

## My role
1. Managing DB by using MySQL and connecting it to web server and chatbot server
2. Making chatbot code with teammate
3. Making and managing AWS EC2 server and S3 server for connecting them with web server, databaser server and AI server

## Why did we start this project?
1. Many patients who had colon polyps should be managed by doctors for preventing colorectal cancer.
2. In present, patients visit hospital and submit handwritten records of their diet and daily lives, but it is pretty difficult that one doctor should check many patients' records.
3. This project's goal is to use chatbot, web server and AI for managing patients' diet and daily lives for the ease of work for doctors. Thus, patients can use medical service regardless of time and place

## Contents
![KakaoTalk_20211206_221423640](https://user-images.githubusercontent.com/86550939/146793576-62ebded6-492c-49f4-85b7-83c88e1d39dd.png)
### 카카오톡 채널 -> KakaoTalk Channel
### AI 서버 -> AI server
### 카카오톡 오픈빌더 -> KakaoTalk Openbuilder
1. First of all, KakaoTalk is kind of Whatsapp in South Korea, and approximately all of Korean people use this app for communication and many other things.
2. We created KakaoTalk chatbot. It receives patient's photo of diet and send it to AI server for analysing which foods are in the photo. After analysing it, AI server sends the photo which has result of the analysis to chatbot and chatbot sends it to patient. After that, patient enters the amount of intake for each food. Finally, chatbot calculates calories, carbohydrate, protein, fat, sodium, calcium, vitamin C and saturated fat and gives the patient feedback of his or her diet. Database has a table which contains the information of nutrition of each food and chatbot use the data in database. This is the way chatbot calculates nutrition. Thus, database saves all the information of nutrition and feedback of each patient in itself.
3. Chatbot also has a survey function. There is a link that patient can conduct the survey for analysing daily life. It asks ten questions for checking whether patient drink enough water or smoke a cigratte and etc. AI analyses answers and give him or her a long feedback.
4. On the webpage, patient can check his or her diet and feedback in the past by selecting the date. Those data is from database and those data was saved in previous steps. Especially, on the webpage, he or she can be recommended a nice food or ingrdient which is good for preventing colorectal cancer. 
5. In the case of doctor, on the webpage, he or she can check the list of patients who he or she manages. By selecting patient, doctor can see the list of diet of patient and he or she can download the diet information which includes numerical nutrition information as csv file.  


### Result
- Won a second 2nd place award among other teams
