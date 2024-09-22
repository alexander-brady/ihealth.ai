import { Message } from "../../chat/page";
import { AvatarGPTIcon } from "../icons/avatarGPTIcon";

type ChatBubbleProps = {
  message: Message;
};

export default function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} my-2 items-start`}>
      {!isUser && (
        <div className="mr-2">
          <AvatarGPTIcon />
        </div>
      )}
      <div
        className={`max-w-[80%] p-2 rounded-lg ${
          isUser ? 'bg-blue-200' : 'bg-gray-200'
        }`}
      >
        <span className="font-serif text-sm md:text-md">{message.text}</span>
      </div>
    </div>
  );
}



