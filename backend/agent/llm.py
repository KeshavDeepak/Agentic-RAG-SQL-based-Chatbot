from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI

#* import the api key
load_dotenv(dotenv_path='backend/.env')

#* an conversational llm
conversational_llm = AzureChatOpenAI(
    api_version='2025-01-01-preview'
)

#* fixed-output llm
fixed_output_llm = AzureChatOpenAI(
    api_version='2025-01-01-preview',
    temperature=0
)

#* test out the conversational llm
if __name__ == '__main__':
    print(conversational_llm.invoke("Why is the sky blue?").content)