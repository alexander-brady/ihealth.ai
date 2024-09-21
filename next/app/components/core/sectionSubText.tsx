'use client';

interface SectionSubTextProps {
  text: string,
}

export default function SectionSubText({text}: SectionSubTextProps){
  return(
    <p className="font-serif text-md md:text-4xl">
      {text}
    </p>
  );
}