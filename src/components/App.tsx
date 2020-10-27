import React, { useEffect, useState } from 'react';
import Socket from './Socket';
import Chat from './Chat';
import Header from './Header';
import Input from './Input';
import Login from './Login';

interface stateType {
    message: string
    name: string
}
interface SingleChatType {
    message: string
    name: string
    email: string
    profilePic: string
}
interface AccountType {
    email: string
    profilePic: string
}

function App() {
  const [state, setState] = useState<stateType>({ name: '', message: '' });
  const [accountInfo, setAccountInfo] = useState<AccountType>({ email: '', profilePic: '' });
  const [chat, setChat] = useState<SingleChatType[]>([]);
  const [totalUsers, setTotalUsers] = useState<number>(0);
  const [loginStatus, setLoginStatus] = useState<boolean>(true);

  useEffect(() => {
    Socket.on('on_connect', (e: any) => {
      setChat(e.messages);
    });

    Socket.on('update_users', (e: any) => {
      setTotalUsers(e.totalUsers);
    });

    Socket.on('message_sent', (e: any) => {
      const {
        name, message, email, profilePic,
      } = e.message;
      return setChat((prevChat) => [...prevChat, {
        name, message, email, profilePic,
      }]);
    });

    Socket.on('on_disconnect', (e: any) => {
      setTotalUsers(e.totalUsers);
    });
    /* eslint-disable no-unused-expressions */
    return () => {
      Socket && Socket.removeAllListeners();
    };
  }, []);

  const onTextChange = (message: string) => {
    setState({ name: state.name, message });
  };

  const onMessageSubmit = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    e.preventDefault();
    const { name, message } = state;
    const { email, profilePic } = accountInfo;
    Socket.emit('message', {
      name, message, email, profilePic,
    });
    setState({ name, message: '' });
  };

  const ifAuthenticated = () => {
    if (loginStatus) {
      return (
        <Login
          setAccountInfo={setAccountInfo}
          setLoginStatus={setLoginStatus}
          setState={setState}
        />
      );
    }
    return (
      <div className="flex flex-col h-screen overflow-x-hidden ">
        <div className="mb-3 bg-gradient-to-b from-gray-900">
          <Header props={[totalUsers, state.name]} />
        </div>
        <div className="flex flex-1 flex-col-reverse overflow-y-auto">
          <Chat chat={chat} state={state} />
        </div>
        <Input
          onTextChange={onTextChange}
          onMessageSubmit={onMessageSubmit}
          message={state.message}
        />
      </div>
    );
  };

  return (
    <div>
      {ifAuthenticated()}
    </div>
  );
}

export default App;
