'use client';

import Button from "../core/button";

export default function LandingNav() {
  return (
    <nav className="w-full hidden md:block">
      <div className="flex justify-between items-center m-auto max-w-screen-xl">
        <div className="ml-5 xl:ml-0">
          <h1 className="text-3xl font-black">iHealth</h1>
        </div>
        <div>
          <ul className="flex flex-row space-x-6">
          {['About', 'Benefits', 'Questions'].map((item) => (
              <li key={item}>
                <a href={`#${item.toLowerCase()}`} className="block text-xl font-black hover:text-blue-600 transition-colors">
                  {item}
                </a>
              </li>
            ))}
          </ul>
        </div>
        <Button 
          text="Sign In!" 
          stylingClass="bg-slate-100 py-3 px-5 my-2 mr-5 xl:mr-0 rounded-md font-black cursor-pointer transition delay-50 hover:bg-slate-200"
          pageRef="/login"
        />
      </div>
    </nav>
  );
}