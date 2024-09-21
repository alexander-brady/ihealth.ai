'use client';

import Link from "next/link";

interface ButtonProps {
  text:string,
  stylingClass: string,
  pageRef: string,
}

export default function Button({ text, stylingClass, pageRef }: ButtonProps) {
  return (
    <div className={stylingClass}>
      <Link href={pageRef}>{text}</Link>
    </div>
  );
}