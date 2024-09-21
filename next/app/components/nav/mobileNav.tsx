'use client';

import { useState } from "react";
import Button from "../core/button";

export default function MobileNav() {
  const [showDropdown, setShowDropdown] = useState(false);

  const Callback = () => {
    setShowDropdown((prev) => !prev);
  }

  return (
      <nav className="w-full block md:hidden">
        <div className='flex justify-between items-center m-auto max-w-screen-xl'>
          <div className="ml-5">
            <h1 className="text-3xl font-black">iHealth</h1>
          </div>
          <button onClick={Callback} className="flex flex-col mr-5 my-2 h-12 w-12 bg-slate-100 rounded-full justify-center items-center relative overflow-hidden">
            <span className={`h-0.5 w-6 my-1 rounded-full bg-black transition ease transform duration-300 ${showDropdown ? "rotate-45 translate-y-2.5" : ""}`}></span>
            <span className={`h-0.5 w-6 my-1 rounded-full bg-black transition ease transform duration-300 ${showDropdown ? "opacity-0" : "opacity-100"}`}></span>
            <span className={`h-0.5 w-6 my-1 rounded-full bg-black transition ease transform duration-300 ${showDropdown ? "-rotate-45 -translate-y-2.5" : ""}`}></span>
          </button>
        </div>
        {showDropdown && (
        <div className="bg-white text-left">
          <ul className="flex flex-col p-6">
            {['About', 'Benefits', 'Questions'].map((item) => (
              <li key={item} className="my-2">
                <a href={`#${item.toLowerCase()}`} className="block text-xl font-black hover:text-blue-600 transition-colors">
                  {item}
                </a>
              </li>
            ))}
          </ul>
          <div className="max-w-[8rem] text-center">
            <Button 
              text="Sign In!" 
              stylingClass="w-full bg-slate-100 py-2 mb-4 ml-5 rounded-md font-black cursor-pointer transition delay-50 hover:bg-slate-200"
            />
          </div>
        </div>
      )}
      </nav>
  );
}