'use client';

import Image from 'next/image';
import HeroImage from "./public/Humaaans - Wireframe.png"
import Button from "./components/core/button";
import Card from './components/core/card';
import LandingNav from "./components/nav/landingNav";
import MobileNav from "./components/nav/mobileNav";
import SectionHeading from "./components/core/sectionHeading";
import SectionSubText from "./components/core/sectionSubText";
import DropDownMenu from './components/core/dropDownMenu';

export default function Home() {
  return (
    <div>
      <LandingNav />
      <MobileNav />

      <section id="hero" className="w-full pt-10 pb-[9.4rem]">
        <div className="max-w-screen-xl mx-auto">
          <div className="relative grid grid-cols-0 md:grid-cols-2 gap-8 mx-5 xl:mx-20">
            <div className="flex flex-col mt-48 text-center md:text-left">
              <h1 className="font-roboto text-4xl md:text-5xl font-black">Meet your digital <span className="text-blue-800">AI</span> health assistant</h1>
              <SectionSubText text="Fight off potential health issues in the long run by gaining insight through our AI doctor!"/>
              <div className="flex flex-col items-center md:items-start">
                <Button text="Start Chatting" stylingClass="py-4 px-4 text-white bg-blue-700 hover:bg-blue-800 mt-8 text-center max-w-48" pageRef="/chat" />
              </div>
            </div>
            <div className="hidden md:block">
              <div className="flex items-center justify-end">
                <Image 
                  src={HeroImage}
                  alt="video call of patient and doctor"
                  className="w-full h-[600px] max-w-md"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="about" className="w-full py-32">
        <div className="text-center max-w-screen-xl mx-auto">
          <h1 className="font-roboto text-4xl md:text-5xl font-black">Why we made iHealth<span className="text-blue-800">.ai</span></h1>
          <div className="mt-10 mx-5 xl:mx-0">
            <SectionSubText text="At iHealth.ai, we believe that understanding your health should be simple, personalized, and proactive. With the increasing ability to track vital health metrics through devices like the iPhone, we wanted to empower individuals to make the most of their data. That’s why we built iHealth.ai—to bridge the gap between raw health data and actionable insights." />
          </div>
        </div>
      </section>

      <section id="benefits" className="w-full py-32">
        <div className="text-center max-w-screen-xl mx-auto">
          <div className="mx-5 xl:mx-0">
            <SectionHeading text="Benefits of our personal assistant"/>
          </div>
            <div className="">
              <div className="grid lg:grid-cols-3 gap-8 mt-20 mx-5 xl:mx-0">
                <Card heading="Early Detection of Health Issues" information="Our AI-powered assistant analyzes your health data in real-time, flagging potential abnormalities that might go unnoticed. This early detection helps you address concerns before they become serious, giving you peace of mind and control over your well-being." />
                <Card heading="Personalized Health Insights" information="iHealth.ai tailors its insights specifically to your health patterns, offering recommendations and trends based on your unique data. Instead of generic advice, you’ll receive information relevant to your lifestyle and personal health journey." />
                <Card heading="Data-Driven Decisions" information="With AI-powered analysis, iHealth.ai helps you make more informed decisions about your health. By offering clear insights into your trends and deviations, our assistant empowers you to have more meaningful conversations with healthcare professionals." />
              </div>
            </div>
        </div>
      </section>

      <section id="questions" className="w-full py-32">
        <div className="text-center max-w-screen-xl mx-auto">
          <SectionHeading text="FAQs"/>
            <div className="mx-5 xl:mx-0">
              <DropDownMenu question="What data does iHealth.ai use from my iPhone?" answer="iHealth.ai accesses your iPhone’s health data, including metrics such as heart rate, sleep patterns, activity levels, steps, and other available health indicators. All data is securely processed to provide personalized insights, and privacy is our top priority."/>
              
              <DropDownMenu question="How does iHealth.ai analyze my health data?" answer="Our platform uses advanced AI algorithms trained to detect patterns, irregularities, and trends in your health data. By comparing your data to both medical guidelines and past trends in your own metrics, iHealth.ai helps identify potential issues before they become major concerns."/>
              
              <DropDownMenu question="Can iHealth.ai diagnose medical conditions?" answer="No, iHealth.ai is not a substitute for professional medical advice or diagnosis. Our tool provides insights and flags potential areas of concern, but it’s important to consult with a healthcare professional for any medical diagnosis or treatment."/>
              
              <DropDownMenu question="How often should I use iHealth.ai?" answer="You can use iHealth.ai as often as you'd like. We recommend using it daily or weekly to monitor trends in your health data. This regular use can help detect any abnormalities or changes over time."/>
              
              <DropDownMenu question="How accurate is the analysis provided by iHealth.ai?" answer="Our AI is designed to offer highly accurate insights based on the data you provide. However, it is important to note that the quality and completeness of the data, as well as the complexity of health, mean that our insights are not infallible. Always consult a medical expert for serious concerns."/>
            </div>
        </div>
      </section>

      <section className="w-full py-32">
        <div className="max-w-screen-xl bg-slate-100 rounded-3xl m-auto py-32 px-16">
          <div className="flex flex-col text-center items-center">
            <SectionHeading text="Go down your health journey today!"/>
            <Button text="Start Chatting!" stylingClass="py-4 px-4 text-white bg-blue-700 hover:bg-blue-800 mt-8 text-center max-w-48" pageRef="/login" />
          </div>
        </div>
      </section>

      <footer className="w-full bg-slate-100 rounded-tl-[5rem] rounded-tr-[5rem] py-32">
        <div className="max-w-screen-xl m-auto flex flex-col text-center ">
          <h1 className="text-3xl font-black">iHealth<span className="text-blue-800">.ai</span></h1>
          <SectionSubText text="Moving towards a better future!"/>
          <p className="font-serif">© 2024 iHealth INC</p>
        </div>
      </footer>
    </div>
  );
}
