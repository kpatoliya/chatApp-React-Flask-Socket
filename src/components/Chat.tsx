import React from 'react';
import '../styles/chat.css';
import parse from 'html-react-parser';

interface SingleChatType {
    message: string
    name: string
    email: string
    profilePic: string
}
interface stateType {
    message: string
    name: string
}
interface ChatType {
    chat: SingleChatType[]
    state: stateType
}

const Chat: React.FC<ChatType> = ({ chat, state }: ChatType) => (
  <div className="h-auto">
    {chat.map((singleChat) => (
      <div className="m-4">
        <div className="flex p-2 flex-col inline-flex mb-3 max-w-md border-opacity-0 rounded-lg
                        overflow-y-auto bg-gray-700"
        >
          <div className="flex space-x-2">
            <img className="rounded-full w-8 h-8" src={singleChat.profilePic} alt="profile pic" />
            <div className="h-auto font-extrabold text-white text-md mr-2 font-sans">{singleChat.name}</div>
          </div>
          <div>
            <div
              className="font-mono mt-1 text-gray-200 text-base h-auto "
            >
              {parse(singleChat.message)}
            </div>
          </div>
        </div>
      </div>
    ))}
  </div>
);

export default Chat;
