'use client';

interface SectionSubTextProps {
  text: string,
}

export default function SectionSubText({text}: SectionSubTextProps){
  return(
    <p className="font-serif text-md md:text-xl mt-3">
      {text}
    </p>
  );
}