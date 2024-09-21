

interface ButtonProps {
  text:string,
}



export default function Button({ text }: ButtonProps) {
  return (
    <div className="bg-slate-100 py-5 px-10">
      {text}
    </div>
  );
}