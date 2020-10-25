import io from 'socket.io-client';

const Socket = io.connect('/');

export default Socket;
