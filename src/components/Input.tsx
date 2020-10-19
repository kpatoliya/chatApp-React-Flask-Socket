import React from "react";

interface InputType {
    onTextChange: (message: string) => void
    onMessageSubmit: (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    message: string
}

const Input: React.FC<InputType> = ({onTextChange, onMessageSubmit, message}) => {

    const onSubmit = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        onMessageSubmit(e)
    }

    const handleKeyPress = (e: any) => {
        if (e.key === 'Enter') {
            onMessageSubmit(e)
        }
    }

    const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onTextChange(e.target.value)
    }

    return (
        <div className="flex w-full m-2 justify-center rounded-lg border-2 border-grey-600 ">
            <button className="hover:bg-gray-200 text-3xl text-grey bg-gray-300 px-3 border-r-2" onClick={onSubmit}>+
            </button>
            <input type="text" className="w-full mr-4 p-4 bg-gray-300 focus:bg-white"
                   placeholder="Message to #general"
                   value={message}
                   onChange={onChange}
                   onKeyPress={handleKeyPress}/>
        </div>
    )
}

export default Input