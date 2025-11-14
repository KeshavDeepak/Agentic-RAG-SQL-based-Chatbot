import ReactMarkdown from "react-markdown";

//* main function
export default function Conversation({ messages }) {
    const conversation_log = [];

    let common_alignment_styling = 'flex w-full mb-2'
    let common_bubble_styling = 'px-3 py-3 rounded-lg max-w-[75%] text-white'

    //* wrap messages with syntax to make it html-ready
    for (let message of messages) {
        if (message.role == 'user') {
            conversation_log.push(
                <div key={message.id} className={`${common_alignment_styling} justify-end`}>
                    <div className={`${common_bubble_styling} mr-10 bg-purple-700`}>
                        {message.content}
                    </div>
                </div>
            )
        } 
        else if (message.role == 'assistant') {
            conversation_log.push(
                <div key={message.id} className={`${common_alignment_styling} justify-start`}>
                    <div className={`${common_bubble_styling} ml-5 prose prose-invert`}>
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>  
                </div>
            )
        }
        else if (message.role == 'system') {
            conversation_log.push(
                <div key={message.id} className={`${common_alignment_styling} justify-center`}>
                    <div className={`${common_bubble_styling} text-3xl font-bold`}>
                        {message.content}
                    </div>
                </div>
            )
        }
    }

    return (
    <div className='pb-[20vh] pt-[5vh]'>  
        {conversation_log}
    </div>
    )
}