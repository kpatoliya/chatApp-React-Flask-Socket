import React from "react";
import GoogleLogin from 'react-google-login';


const GoogleAuth:React.FC<any> = () => {

    const responseGoogle = (response: any) => {
        console.log(response.nt.Ad)
        console.log(response.nt.Wt)
        console.log(response.profileObj.imageUrl)
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