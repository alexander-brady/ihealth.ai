'use client';

import { useState } from "react";
import SectionHeading from "./sectionHeading";
import SectionSubText from "./sectionSubText";

interface DropDownMenuProps{
  question: string,
  answer: string,
}

export default function DropDownMenu({question, answer}: DropDownMenuProps){

  const [showDropdown, setShowDropdown] = useState(false);

  const Callback = () => {
    setShowDropdown((prev) => !prev);
  }

  return(
    <div>
      <div className={` bg-slate-50 mt-10 ${showDropdown ? 'rounded-tl-md rounded-tr-md' : 'rounded-md'}`}>
        <div onClick={Callback} className="flex justify-between items-center p-4">
          <SectionHeading text={question}/>
          <button className="flex flex-col h-12 w-12 bg-slate-100 rounded-lg justify-center items-center relative overflow-hidden">
            <span className={`absolute h-0.5 w-6 rounded-full bg-blue-700 transition-all duration-300 ${showDropdown ? 'rotate-0' : 'rotate-0'}`}></span>
            <span className={`absolute h-0.5 w-6 rounded-full bg-blue-700 transition-all duration-300 ${showDropdown ? 'rotate-0' : '-rotate-90'}`}></span>
          </button>
        </div>
      </div>
      
      
      {showDropdown && (
        <div className="bg-slate-50 text-left rounded-bl-md rounded-br-md">
          <div className="p-4">
            <SectionSubText text={answer} />
          </div>
        </div>
      )}
    </div>
  );
}