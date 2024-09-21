'use client';

import Button from "../core/button";

export default function LandingNav() {
  return (
    <nav className="w-full hidden md:block">
      <div className="flex justify-between items-center m-auto max-w-screen-xl">
        <div className="ml-5 xl:ml-0">
          <h1 className="text-3xl font-black">iHealth<span className="text-blue-800">.ai</span></h1>
        </div>
        <div>
          <ul className="flex flex-row space-x-6">
          {['About', 'Benefits', 'Questions'].map((item) => (
              <li key={item}>
                <a href={`#${item.toLowerCase()}`} className="block text-xl font-black duration-300 hover:text-blue-800 transition-colors">
                  {item}
                </a>
              </li>
            ))}
          </ul>
        </div>
        <Button 
          text="Sign In!" 
          stylingClass="text-white bg-blue-700 hover:bg-blue-800 py-3 px-5 my-2 mr-5 xl:mr-0"
          pageRef="/login"
        />
      </div>
    </nav>
  );
}