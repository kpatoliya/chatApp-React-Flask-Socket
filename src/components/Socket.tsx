import io from 'socket.io-client';

const Socket = io.connect('http://localhost:4000');

export default Socket;
