import { useState } from "react"

function Chatbox({ handleNewQuestion, messages }) {
    //* stores the user's live input
    const [input, setInput] = useState('');

    //* when user presses enter
    const handleSubmit = (e) => {
        e.preventDefault(); //* ensures page does not refresh

        if (!input.trim()) return; //* ignore empty messages

        handleNewQuestion(input); //* call parent component's function to handle user input

        setInput(""); //* clear the input
    }

    return <div>
        <form id='chatbox-form' onSubmit={handleSubmit}
            className='fixed bottom-[5vh] w-full flex justify-center'>
            <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key == "Enter" && !e.shiftKey) { //* return question if enter is pressed
                        e.preventDefault(); //* prevent new line
                        handleSubmit(e); //* call handleSubmit instead
                    }
                }}
                onInput={(e)=>{
                    e.target.style.height = 'auto'; //* ensures height goes down on deletion of input
                    e.target.style.height = `${e.target.scrollHeight}px`; //* matches scroll height
                }}
                placeholder="Ask me anything"
                className='bg-black border-2 border-blue-500 p-3 rounded-xl w-1/2 outline-none resize-none max-h-[40vh] overflow-y-auto'
            />
        </form>
    </div>
}

export default Chatbox