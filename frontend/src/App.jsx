// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'

import { useState, useEffect } from 'react'

import Conversation from './components/Conversation.jsx'
import Chatbox from './components/Chatbox.jsx'

import './App.css'

export default function App() {
	//* holds the conversation so far
	const [messages, setMessages] = useState([
		{'id' : 1, 'role' : 'system', 'content' : "You're connected to the AdventureWorks database. Ask me anything!"}
	]);

	//* auto-scrolls when new messages cause overflow
	useEffect(() => {
		window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth'});
	}, [messages]);

	//* handles an incoming question
	const handleNewQuestion = (question) => {
		let messages_length = messages.length;

		//* transform the incoming question into a message
		let question_message = {
			id : messages_length + 1,
			role : 'user',
			content : question,
		};

		setMessages((messages) => [...messages, question_message])

		//* send to backend and receive an answer back
		sendToBackend([...messages, question_message]).then(response => {
			//* transform the response into a message
			let response_message = {
				id : messages_length + 2,
				role : 'assistant',
				content : response.messages[response.messages.length-1].content
			};

			//* append response to messages
			setMessages((messages) => [...messages, response_message]);
		})
	}
	

	return (
	<div className='flex flex-col w-screen h-screen'>
		<Conversation messages={messages}/>
		<Chatbox handleNewQuestion={handleNewQuestion} messages={messages}/>
	</div>)
}

//* send a question to the backend and receive an answer
const sendToBackend = async (messages) => {
	var response = await fetch(
		'http://127.0.0.1:8000/invoke-agent',
		{
			method : 'POST',
			headers : { 'content-type' : 'application/json' },
			body : JSON.stringify({
				messages : messages
			})
		}
	);

	var full_response = await response.json();

	return full_response;
}