import { useState } from "react"

function Chatbox({ handleNewQuestion }) {
    //* stores the user's live input
    const [input, setInput] = useState('');

    //* when user presses enter
    const handleSubmit = (e) => {
        e.preventDefault(); //* ensures page does not refresh

        if (!input.trim()) return; //* ignore empty messages

        handleNewQuestion(input); //* call parent component's function to handle user input

        setInput(""); //* clear the input
    }

    return <>
        <form id='chatbox-form' onSubmit={handleSubmit}>
            <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key == "Enter" && !e.shiftKey) { //* return question if enter is pressed
                        e.preventDefault(); //* prevent new line
                        handleSubmit(e); //* call handleSubmit instead
                    }
                }}
                placeholder="Ask something"
            />
        </form>
    </>
}

export default Chatbox