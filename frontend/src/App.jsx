// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'

import { useState } from 'react'

import Conversation from './components/Conversation.jsx'
import Chatbox from './components/Chatbox.jsx'

import './App.css'

export default function App() {
	//* holds the conversation so far
	const [messages, setMessages] = useState([]);

	//* handles an incoming question
	const handleNewQuestion = (question) => {
		let messages_length = messages.length;

		//* transform the incoming question into a message
		let question_message = {
			id : messages_length + 1,
			role : 'user',
			content : question,
		};

		//* append to messages
		setMessages((messages) => [...messages, question_message]);

		//* send to backend and receive an answer back
		sendToBackend(question).then(response => {
			//* transform the response into a message
			let response_message = {
				id : messages_length + 2,
				role : 'assistant',
				content : response.messages[response.messages.length-1].content
			};

			//* append to messages
			setMessages((messages) => [...messages, response_message]);
		})
	}
	

	return <>
		<Conversation messages={messages}/>
		<Chatbox handleNewQuestion={handleNewQuestion}/>
	</>
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


/*
const [count, setCount] = useState(0)

  return (
	<>
	  <div>
		<a href="https://vite.dev" target="_blank">
		  <img src={viteLogo} className="logo" alt="Vite logo" />
		</a>
		<a href="https://react.dev" target="_blank">
		  <img src={reactLogo} className="logo react" alt="React logo" />
		</a>
	  </div>
	  <h1>Vite + React</h1>
	  <div className="card">
		<button onClick={() => setCount((count) => count + 1)}>
		  count is {count}
		</button>
		<p>
		  Edit <code>src/App.jsx</code> and save to test HMR
		</p>
	  </div>
	  <p className="read-the-docs">
		Click on the Vite and React logos to learn more
	  </p>
	</>
  )
*/
