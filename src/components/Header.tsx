import React from 'react';

interface HeaderType {
    props: [number, string]
}

const Header: React.FC<HeaderType> = ({ props }) => (

  <div className="flex flex-row place-items-auto items-center">
    <div className="flex-1 p-3 m-3 font-serif text-white text-xl font-extrabold">
      #general
    </div>
    <div className="flex-1 items-center text-center text-c p-3 m-3 font-serif text-gray-400 text-xl ">
      {props[1]}
    </div>
    <div className="flex-1 text-right font-serif text-white text-xl p-3 m-3">
      <span className="text-green-500 text-xl">● </span>
      Online:
      {' '}
      {props[0]}
    </div>
  </div>

);

export default Header;
