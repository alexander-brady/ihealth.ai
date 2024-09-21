'use client';

interface ButtonProps {
  text:string,
  stylingClass: string,
}

export default function Button({ text, stylingClass }: ButtonProps) {
  return (
    <div className={stylingClass}>
      {text}
    </div>
  );
}