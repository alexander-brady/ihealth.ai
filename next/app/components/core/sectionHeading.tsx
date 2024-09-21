'use client';

interface SectionHeadingProps {
  text: string,
}

export default function SectionHeading({text}: SectionHeadingProps){
  return(
    <h1 className="font-roboto text-xl md:text-3xl">
      {text}
    </h1>
  );
}