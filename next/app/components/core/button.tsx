'use client';

import Link from "next/link";

interface ButtonProps {
  text:string,
  stylingClass: string,
  pageRef: string,
}

export default function Button({ text, stylingClass, pageRef }: ButtonProps) {
  const defaultStyles = "rounded-md font-black cursor-pointer transition duration-300 hover:bg-slate-200";


  return (
    <div className={`${defaultStyles} ${stylingClass}`}>
      <Link href={pageRef}>{text}</Link>
    </div>
  );
}