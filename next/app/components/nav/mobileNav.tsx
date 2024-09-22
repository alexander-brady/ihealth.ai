'use client';

import { useState } from "react";
import Button from "../core/button";

import { useUser } from "@propelauth/nextjs/client";

export default function MobileNav() {
  const [showDropdown, setShowDropdown] = useState(false);

  const { user } = useUser();

  const Callback = () => {
    setShowDropdown((prev) => !prev);
  }

  return (
      <nav className="w-full block md:hidden">
        <div className='flex justify-between items-center m-auto max-w-screen-xl'>
          <div className="ml-5">
            <h1 className="text-3xl font-black">iHealth<span className="text-blue-800">.ai</span></h1>
          </div>
          <button onClick={Callback} className="flex flex-col mr-5 my-3 h-12 w-12 bg-slate-100 rounded-full justify-center items-center relative overflow-hidden">
            <span className={`h-0.5 w-6 my-1 rounded-full bg-blue-800 transition ease transform duration-300 ${showDropdown ? "rotate-45 translate-y-2.5" : ""}`}></span>
            <span className={`h-0.5 w-6 my-1 rounded-full bg-blue-800 transition ease transform duration-300 ${showDropdown ? "opacity-0" : "opacity-100"}`}></span>
            <span className={`h-0.5 w-6 my-1 rounded-full bg-blue-800 transition ease transform duration-300 ${showDropdown ? "-rotate-45 -translate-y-2.5" : ""}`}></span>
          </button>
        </div>
        {showDropdown && (
        <div className="bg-white text-left h-[100vh]">
          <ul className="flex flex-col p-6">
            {['About', 'Benefits', 'Questions'].map((item) => (
              <li key={item} className="my-2">
                <a onClick={Callback} href={`#${item.toLowerCase()}`} className="block text-xl font-black duration-300 hover:text-blue-600 transition-colors">
                  {item}
                </a>
              </li>
            ))}
          </ul>
          <div className="max-w-[8rem] text-center">
            { !user &&
              <Button 
                text="Sign In!" 
                stylingClass="text-white bg-blue-700 hover:bg-blue-800 py-3 px-5 my-2 mr-5 xl:mr-0"
                pageRef="/api/auth/login"
              />
            }
          </div>
        </div>
      )}
      </nav>
  );
}