# iHealth.ai
### Created by Alexander Brady, Alexandre Payumo, Hung Que Dang, and Jordan Yin

## Inspiration
92% of Americans don’t undergo routine health screenings. In fact, missed preventative opportunities cost US healthcare 55 billion dollars every year. We wanted to create a proactive solution that uses the data we already generate through devices like iPhones and Apple Watches. Our goal was to provide people with daily insights into their health, helping them make informed decisions about whether to visit a doctor or change their habits before more serious issues arise.

## Description of our Web App
iHealth.ai automatically collects daily health data, such as heart rate, sleep analysis, walking distance, and headphone audio exposure, from Apple devices. It then processes this data and feeds it into a powerful language model (LLM). The LLM analyzes patterns and provides actionable insights, recommending whether you should seek medical advice or take steps to improve your health.

# Stack
### Frontend
- Next.JS
    - Typescript
- Tailwind CSS
 
### Backend
- MongoDB
- Flask
- GPT-4o
- PropelAuth
- LangChain

# How we built it
We used PropelAuth to authenticate users securely and Vercel to host our web application. Apple HealthKit APIs were used to gather health data from users' iPhones and Apple Watches, such as heart rate, sleep duration, walking distance, and audio exposure. This data is stored securely in MongoDB. We then used OpenAI's API to analyze the data, providing users with feedback based on their health trends.

# Challenges we ran into
One of the biggest challenges we encountered was implementing Propel Auth0 for user authentication. Integrating it across platforms was far more complex than expected, particularly when trying to synchronize user sessions and securely manage health data from Apple devices. Initially, we planned to use the Cerebras AI model for health analysis, but soon realized it was too computationally demanding to run on our laptops, requiring us to pivot to OpenAI's GPT model. Additionally, we faced challenges with parsing and cleaning health data from Apple’s XML files. The raw format required custom parsers to extract and organize data, such as sleep, heart rate, and walking metrics, so that it could be fed into the AI model effectively. While time-consuming and technically demanding, this process was crucial to ensuring accurate and reliable health assessments.

# Accomplishments that we're proud of
We’re proud of the seamless integration of multiple technologies: Apple HealthKit, MongoDB, Flask, Propel Auth0, and OpenAI’s API. Our team worked hard to ensure that the daily health updates are user-friendly, and the insights are actionable. We’ve made healthcare more accessible by giving people insights without having to schedule constant check-ups.

# What we learned
We learned a lot about the complexity of health data and how to present it in a way that is both accessible and meaningful to users. We also deepened our understanding of integrating machine learning models with real-world data and handling large datasets in a secure, scalable way.

# What's next for iHealth.ai
We plan to team up with actual doctors to fine-tune our model and provide better, more medically tailored recommendations. By collaborating with medical professionals, we hope to make iHealth.ai more accurate and helpful, using a specialized GPT model to assess patient health with greater precision. Our ultimate goal is to create a personalized health advisor that everyone can access, no matter where they are or how often they visit a doctor.

# Landing Page
![image](https://github.com/user-attachments/assets/031b34d4-133b-41b6-9658-20acc0870012)
![image](https://github.com/user-attachments/assets/61bf4189-c346-42fe-b3bf-e9ab13d74960)
![image](https://github.com/user-attachments/assets/3791dcdc-f762-4f90-a99f-4235fb2dd46e)

# Upload Page
![image](https://github.com/user-attachments/assets/79ec6b1f-18b2-4ffe-a3d0-8b3fb4ec0403)

# Chat Bot Page
![image](https://github.com/user-attachments/assets/a1522a4b-99d9-45c9-8f97-7c4ac6864333)



