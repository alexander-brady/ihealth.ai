'use client';

import SectionHeading from "./sectionHeading";
import SectionSubText from "./sectionSubText";

interface CardProps{
  heading: string,
  information: string
}


export default function Card({heading, information}: CardProps){
  return(
    <div className="bg-slate-100 rounded-md shadow-md">
      <div className="p-6">
        <SectionHeading text={heading} />
        <SectionSubText text={information} />
      </div> 
    </div>
  );
}