import React from 'react';
import GoogleLogin from 'react-google-login';
import FontAwesome from 'react-fontawesome';
import Socket from './Socket';

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

const GoogleAuth:React.FC<GoogleAuthType> = (
  { setAccountInfo, setLoginStatus, setState }: GoogleAuthType,
) => {
  const responseGoogle = (response: any) => {
    setLoginStatus(false);
    setState({ name: response.profileObj.name, message: '' });
    setAccountInfo({ email: response.profileObj.email, profilePic: response.profileObj.imageUrl });
    Socket.emit('update_total_users', response.profileObj.email);
  };

  return (
    <div className="align-middle">
      <GoogleLogin
        clientId="955471402983-pei3u5jmjvjq6uiruv8dv4mdlch9ebig.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={responseGoogle}
        cookiePolicy="single_host_origin"
      >
        <FontAwesome name="google" />
        <span> Login with Google</span>
      </GoogleLogin>
    </div>
  );
};
export default GoogleAuth;
