import React, {useEffect, useState} from 'react';
import Socket from './Socket';
import Chat from './Chat';
import Header from "./Header";
import Input from "./Input";
import GoogleAuth from "./GoogleAuth";
import FacebookAuth from "./FacebookAuth";

interface stateType {
    message: string
    name: string
}
interface SingleChatType {
    message: string
    name: string
    profilePic: string
}
interface AccountType {
    email: string
    profilePic: string
}

function App() {
    const [state, setState] = useState<stateType>({name: '', message: ''})
    const [accountInfo, setAccountInfo] = useState<AccountType>({email: '', profilePic: ''})
    const [chat, setChat] = useState<SingleChatType[]>([])
    const [totalUsers, setTotalUsers] = useState<number>(0)
    const [loginStatus, setLoginStatus] = useState<boolean>( true)
    const [sid, setSid] = useState<string>('')

    useEffect(() => {

        Socket.on('on_connect', (e: any) => {
            setChat(e.messages)
            setSid(e.sid)
        })

        Socket.on('update_users', (e: any) => {
            setTotalUsers(e.totalUsers)
        })

        Socket.on('message_sent', (e: any) => {
            const {name, message, email, profilePic} = e.message
            return setChat(prevChat => [...prevChat, {name, message, profilePic}]);
        })

        Socket.on('on_disconnect', (e: any) => {
            setTotalUsers(e.totalUsers)
        })

        return () => {
              Socket && Socket.removeAllListeners()
          }

    },[])

    const onTextChange = (message: string) => {
        setState({name: state.name, message: message})
    }

    const onMessageSubmit = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.preventDefault()
        const {name, message} = state
        const {email, profilePic} = accountInfo
        Socket.emit('message', {name, message, email, profilePic})
        setState({name, message: ''})
    }

    const ifAuthenticated = () => {
        if(loginStatus) {
            return (
                <React.Fragment>
                    <div className="bg-gray-200 w-screen h-screen flex justify-center items-center">
                        <div className="w-1/3 justify-center">
                            <h1 className="font-hairline mb-6 font-extrabold text-4xl text-left">Login to ChatApp</h1>
                            <GoogleAuth setAccountInfo={setAccountInfo} setLoginStatus={setLoginStatus} setState={setState}/>
                            <FacebookAuth setAccountInfo={setAccountInfo} setLoginStatus={setLoginStatus} setState={setState}/>
                        </div>
                    </div>
                </React.Fragment>
            )
        }else {
            return (
                <div className="flex flex-col h-screen overflow-x-hidden ">
                    <div className="mb-3 bg-gradient-to-b from-gray-900">
                        <Header props={[totalUsers, state.name]}/>
                    </div>
                    <div className="flex flex-1 flex-col-reverse overflow-y-auto">
                        <Chat chat={chat} />
                    </div>
                    <Input onTextChange={onTextChange} onMessageSubmit={onMessageSubmit} message={state.message}/>
                </div>
            )
        }
    }
    return(
        <div>
            {ifAuthenticated()}
        </div>
    )
}

export default App;