function Conversation({ messages }) {
    const conversation_log = [];

    //* wrap messages with syntax to make it html-ready
    for (let message of messages) {
        conversation_log.push(
            <div key={message.id}>
                {message.content}
            </div>
        )
    }

    return (
    <>
        {/* <div className="p-4 mb-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold rounded-xl shadow-lg">
            Tailwind is working
        </div> */}
        
        {conversation_log}
    </>
    )
}

export default Conversation