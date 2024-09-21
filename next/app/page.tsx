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
              <SectionHeading text="Meet your digital AI health assistant"/>
              <SectionSubText text="Fight off potential health issues in the long run by gaining insight through our AI doctor!"/>
              <div className="flex flex-col items-center md:items-start">
                <Button text="Start Chatting" stylingClass="py-4 px-4 bg-slate-100 mt-8 text-center max-w-48" pageRef="/login" />
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
          <SectionHeading text="Why we made iHealth"/>
          <div className="mt-10 mx-5 xl:mx-0">
            <SectionSubText text="Lorem ipsum odor amet, consectetuer adipiscing elit. Tempus congue ad ut imperdiet; quisque habitant. Metus ligula suscipit libero, ultrices metus ornare. Tortor turpis viverra mollis cubilia mattis. Condimentum porttitor enim mollis ut, aliquet mattis? Lorem urna efficitur aptent; viverra dolor ex. Egestas ornare non, magnis suscipit est interdum donec integer iaculis. Curabitur pulvinar dictum velit penatibus consequat. Arcu faucibus placerat dignissim amet bibendum pellentesque." />
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
                <Card heading="Accuracy" information="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac." />
                <Card heading="Accuracy" information="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac." />
                <Card heading="Accuracy" information="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac." />
              </div>
            </div>
        </div>
      </section>

      <section id="questions" className="w-full py-32">
        <div className="text-center max-w-screen-xl mx-auto">
          <SectionHeading text="FAQs"/>
            <div className="mx-5 xl:mx-0">
              <DropDownMenu question="FAQ" answer="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac."/>
              <DropDownMenu question="FAQ" answer="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac."/>
              <DropDownMenu question="FAQ" answer="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac."/>
              <DropDownMenu question="FAQ" answer="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac."/>
              <DropDownMenu question="FAQ" answer="Lorem ipsum odor amet, consectetuer adipiscing elit. Magna ridiculus condimentum aenean penatibus tempus imperdiet justo vulputate. Mus eget pharetra mattis rhoncus vulputate neque hac."/>
            </div>
        </div>
      </section>

      <section className="w-full py-32">
        <div className="max-w-screen-xl bg-slate-100 rounded-3xl m-auto py-32 px-16">
          <div className="flex flex-col text-center items-center">
            <SectionHeading text="Go down your health journey today!"/>
            <Button text="Start Chatting!" stylingClass="py-4 px-4 bg-slate-200 mt-8 text-center max-w-48" pageRef="/login" />
          </div>
        </div>
      </section>

      <footer className="w-full bg-slate-100 rounded-tl-[5rem] rounded-tr-[5rem] py-32">
        <div className="max-w-screen-xl m-auto flex flex-col text-center ">
          <SectionHeading text="iHealth" />
          <SectionSubText text="Moving towards a better future!"/>
          <p className="font-serif">© 2024 iHealth INC</p>
        </div>
      </footer>
    </div>
  );
}
