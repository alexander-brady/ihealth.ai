'use client';

import SectionHeading from "./sectionHeading";
import SectionSubText from "./sectionSubText";

interface CardProps{
  heading: string,
  information: string,
  children: React.ReactNode
}


export default function Card({heading, information, children}: CardProps){
  return(
    <div className="bg-slate-100 rounded-md shadow-md">
      <div className="flex flex-col items-center mt-10">
        {children}
      </div>
      <div className="p-6 text-center">
        <SectionHeading text={heading} />
        <SectionSubText text={information} />
      </div> 
    </div>
  );
}