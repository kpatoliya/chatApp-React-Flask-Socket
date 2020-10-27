import React from 'react';
import FacebookLogin from 'react-facebook-login';
import Socket from './Socket';

interface AccountType {
    email: string
    profilePic: string
}
interface SingleChatType {
    message: string
    name: string
}
interface FacebookAuthType {
    setAccountInfo: (e: AccountType) => void
    setLoginStatus: (e: boolean) => void
    setState: (e: SingleChatType) => void
}

const FacebookAuth:React.FC<FacebookAuthType> = (
  { setAccountInfo, setLoginStatus, setState }: FacebookAuthType,
) => {
  const responseFacebook = (response: any) => {
    setLoginStatus(false);
    setState({ name: response.name, message: '' });
    setAccountInfo({ email: response.email, profilePic: response.picture.data.url });
    Socket.emit('update_total_users', response.email);
  };

  const failureFacebook = () => (
    // eslint-disable-next-line no-alert
    alert('Failed to login')
  );

  return (
    <div className="align-middle">
      <FacebookLogin
        appId="856995921505171"
        autoLoad={false}
        fields="name,email,picture"
        callback={responseFacebook}
        onFailure={failureFacebook}
        cookie={false}
      />
    </div>
  );
};
export default FacebookAuth;
