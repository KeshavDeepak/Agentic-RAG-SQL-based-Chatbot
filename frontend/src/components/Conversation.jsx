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

    return <>
        {conversation_log}
    </>
}

export default Conversation