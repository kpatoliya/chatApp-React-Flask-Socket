import React from "react";
import GoogleLogin from 'react-google-login';
import Socket from "./Socket";
import FontAwesome from "react-fontawesome";

interface AccountType {
    email: string
    profilePic: string
}
interface SingleChatType {
    message: string
    name: string
}

interface GoogleAuthType {
    setAccountInfo: (e: AccountType) => void
    setLoginStatus: (e: boolean) => void
    setState: (e: SingleChatType) => void
}

const GoogleAuth:React.FC<GoogleAuthType> = ({setAccountInfo, setLoginStatus, setState}) => {

    const responseGoogle = (response: any) => {
        console.log(response.nt.Ad)
        setLoginStatus( false)
        setState({name: response.nt.Ad, message: ''})
        setAccountInfo({email: response.nt.Wt, profilePic: response.profileObj.imageUrl})
        Socket.emit('update_total_users', response.nt.Wt)
    }


    return(
        <div className="align-middle">
            <GoogleLogin
            clientId="955471402983-3ij9nsbi3gsds15h189e6nnnj7tpguud.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={responseGoogle}
            cookiePolicy={'single_host_origin'} >
            <FontAwesome
                name='google' />
            <span> Login with Google</span>
            </GoogleLogin>
        </div>
    )
}
export default GoogleAuth;