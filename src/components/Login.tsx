import React from "react";
import FacebookAuth from "./FacebookAuth";
import GoogleAuth from "./GoogleAuth";

interface AccountType {
    email: string
    profilePic: string
}
interface SingleChatType {
    message: string
    name: string
}
interface LoginType {
    setAccountInfo: (e: AccountType) => void
    setLoginStatus: (e: boolean) => void
    setState: (e: SingleChatType) => void
}

const Login:React.FC<LoginType> = ({setAccountInfo, setLoginStatus, setState}) => {

    return(
        <React.Fragment>
            <div className="bg-gray-200 w-screen h-screen flex flex-col justify-center items-center">
                <h1 className="font-hairline mb-6 font-extrabold text-4xl text-left">Login to ChatApp</h1>
                <div className="flex-col flex ">
                    <GoogleAuth setAccountInfo={setAccountInfo} setLoginStatus={setLoginStatus} setState={setState}/>
                    <FacebookAuth setAccountInfo={setAccountInfo} setLoginStatus={setLoginStatus} setState={setState}/>
                </div>
            </div>
        </React.Fragment>
    )
}

export default Login;