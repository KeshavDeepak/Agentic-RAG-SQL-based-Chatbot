from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.agent.build_graph import agent

#* fastapi app
app = FastAPI()

#* allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  #* frontend URL
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#* endpoint that invokes the agent on a user question and returns back the answer
@app.post('/invoke-agent')
async def invoke_agent(request: Request):
    #* extract the user question
    full_request = await request.json()
    messages = full_request.get('messages', '')
    
    #* invoke the agent
    response = agent.invoke({'messages' : messages})
    
    #* return the resopnse
    return response