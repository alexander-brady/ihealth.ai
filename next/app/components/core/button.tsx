'use client';

import Link from "next/link";

interface ButtonProps {
  text: string;
  stylingClass: string;
  pageRef?: string; // Make pageRef optional to allow for buttons that only use onClick
  onClick?: () => void; // Add onClick prop
}

export default function Button({ text, stylingClass, pageRef, onClick }: ButtonProps) {
  const defaultStyles = "rounded-md font-black cursor-pointer transition duration-300";

  return (
    <div 
      className={`${defaultStyles} ${stylingClass}`} 
      onClick={onClick} // Handle the click event
    >
      {pageRef ? (
        <Link href={pageRef}>{text}</Link> // Use Link if pageRef is provided
      ) : (
        <span>{text}</span> // Just show the text if no pageRef
      )}
    </div>
  );
}
