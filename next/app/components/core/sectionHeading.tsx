'use client';

interface SectionHeadingProps {
  text: string,
}

export default function SectionHeading({text}: SectionHeadingProps){
  return(
    <h1 className="font-roboto text-4xl md:text-5xl font-black">
      {text}
    </h1>
  );
}