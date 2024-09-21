'use client';

import SectionHeading from "./sectionHeading";
import SectionSubText from "./sectionSubText";

interface CardProps{
  heading: string,
  information: string
}


export default function Card({heading, information}: CardProps){
  return(
    <div className="bg-slate-100 rounded-md">
      <div className="">
        <SectionHeading text={heading} />
        <SectionSubText text={information} />
      </div> 
    </div>
  );
}