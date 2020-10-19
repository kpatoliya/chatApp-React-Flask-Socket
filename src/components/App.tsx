import React, {useEffect, useRef, useState} from 'react';
import io from 'socket.io-client';
import Chat from './Chat';
import Header from "./Header";
import Input from "./Input";
import GoogleAuth from "./GoogleAuth";

interface SingleChatType {
    message: string
    name: string
}


function App() {
    const [state, setState] = useState<SingleChatType>({name: '', message: ''})
    const [chat, setChat] = useState<SingleChatType[]>([])
    const [totalUsers, setTotalUsers] = useState<number>(0)
    const [loginStatus, setLoginStatus] = useState<boolean>(true)
    const socket = useRef<SocketIOClient.Socket>()

    useEffect(() => {
        socket.current = io.connect('http://localhost:4000')
        socket.current.on('on_connect', (e: any) => {
            setTotalUsers(e.totalUsers)
            setState({name: e.userName, message: ''})
            setChat(e.messages)
        })

        socket.current.on('update_users', (e: any) => {
            setTotalUsers(e.totalUsers)
        })

        socket.current.on('message_sent', (e: any) => {
            setTotalUsers(e.totalUsers)
            const {name, message} = e.message
            return setChat(prevChat => [...prevChat, {name, message}]);
        })

        socket.current.on('on_disconnect', (e: any) => {
            setTotalUsers(e.totalUsers)
        })

        return () => {
              socket.current && socket.current.removeAllListeners()
          }

    }, [])

    const onTextChange = (message: string) => {
        setState({name: state.name, message: message})
    }

    const onMessageSubmit = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.preventDefault()
        const {name, message} = state
        socket.current && socket.current.emit('message', {name, message})
        setState({name, message: ''})
    }


    const ifAuthenticated = () => {
        if(loginStatus) {
            return (
                <React.Fragment>
                    <div className="bg-gray-200 h-screen">
                        <GoogleAuth/>
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
                        <Chat chat={chat}/>
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