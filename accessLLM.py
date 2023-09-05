from langchain.schema.document import Document
from langchain.chains.question_answering import load_qa_chain
import os
from langchain.llms import Minimax
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate
)

os.environ["OPENAI_API_KEY"] = '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'
os.environ["MINIMAX_API_KEY"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoibmV3IiwiU3ViamVjdElEIjoiMTY5Mzc1OTYzMzgwMDk1OCIsIlBob25lIjoiTVRNeE16WXlNVFF4TVRrPSIsIkdyb3VwSUQiOiIxNjkzNzU5NjMzNDEyNDMyIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoic2N5aGoxQG5vdHRpbmdoYW0uZWR1LmNuIiwiQ3JlYXRlVGltZSI6IjIwMjMtMDktMDQgMDA6NDk6MjYiLCJpc3MiOiJtaW5pbWF4In0.jI2LFLm9peArggLY7pBpBjT0413ETpb_DhC63VOaiu8K65RMsGya0wrgfV0CoenYz0uZCvhL_rQnHN_EDhdNi3CGs5OlwzynUFwWx-tKgFsxrvgMdsTV92YHDWQdssSlObtC7Jr8YhMwSr5L1uSnICBXgLB5iyco_mGeaXXhyDDTJeRANEfZ5G_FUmm14l6d4ZW72SdBgUEYEjsnhrEK-4JGHAs_66cY8pBa3TUMftJFOyTJ0JO0cnsnMlusWYYoXxhZNjRCtc9NIersX1aCHdNL5VsWYFCrWxEXZFI3LLst8Imll_05w50U2-AQCi7IlnTobamyayTwOhFZmr8hCA"
os.environ["MINIMAX_GROUP_ID"] = "1693759633412432"

def MiniMax(question, input_documents):
    llm = Minimax()

    chain = load_qa_chain(llm,  chain_type="stuff", verbose=True)

    input_documents = [Document(page_content=doc) for doc in input_documents]

    result = chain.run(input_documents=input_documents, question=question)
    return result

def Openai():
    system_template = """
    Use the following context to answer the user's question.
    If you don't know the answer, say you don't, don't try to make it up. And answer in Chinese.
    -----------
    {question}
    -----------
    {chat_history}
    """

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template('{question}')
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
    ConversationalRetrievalChain.from_llm()