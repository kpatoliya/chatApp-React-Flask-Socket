import React from "react";
import GoogleLogin from 'react-google-login';

interface AccountType {
    email: string
    profilePic: string
}

interface GoogleAuthType {
    setAccountInfo: (e: AccountType) => void
}

const GoogleAuth:React.FC<GoogleAuthType> = ({setAccountInfo}) => {

    const responseGoogle = (response: any) => {
        console.log(response.nt.Ad)
        setAccountInfo({email: response.nt.Wt, profilePic: response.profileObj.imageUrl})
    }

    return(
        <div>
            <GoogleLogin
            clientId="955471402983-3ij9nsbi3gsds15h189e6nnnj7tpguud.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={responseGoogle}
            onFailure={responseGoogle}
            cookiePolicy={'single_host_origin'}
            />
        </div>
    )
}
export default GoogleAuth;