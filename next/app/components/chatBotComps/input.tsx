import SendIcon from "../icons/send"

interface InputAreaProps {
  input: string;
  setInput: (value: string) => void;
  sendMessage: () => void;
}

export default function InputArea({
  input,
  setInput,
  sendMessage,
  disabled
}: InputAreaProps) {
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
    <div className="flex w-full max-w-screen-lg mx-auto  items-center">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          disabled={disabled}
          className="rounded-lg w-full bg-slate-100 h-12 resize-none border-0 px-4 py-2.5 mr-4"
        />
      <button
        onClick={sendMessage}
        className="py-2.5 px-2.5 flex-col items-center text-white bg-blue-700 hover:bg-blue-800 rounded-md transition duration-300"
      >
        <SendIcon />
      </button>
    </div>
    <div className="max-w-screen-lg mx-auto text-center pt-1 text-stone-400 text-xs">
      iHealth.ai can make mistakes. For serious health concerns, please reach out to your healthcare provider.
    </div>
    </>
  );
}

