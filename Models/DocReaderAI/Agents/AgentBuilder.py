from langchain_openai import OpenAI
from Helpers.Textor import Textor
from pydantic import BaseModel, Field
from langchain.chains import RetrievalQA
from langchain.agents import AgentType, Tool, initialize_agent

from langchain.globals import set_debug

set_debug(True)


class DocumentInput(BaseModel):
    question: str = Field()


llm = OpenAI(temperature=0)


class AgentBuilder:

    @staticmethod
    def build(loadedFiles):

        docsVS = Textor.transform2Vectors(loadedFiles[0])
        retriver = docsVS.as_retriever()
        tools = [
            Tool(
                args_schema=DocumentInput,
                name="test-name",
                description=f"useful when you want to answer questions about test-name",
                func=RetrievalQA.from_chain_type(llm=llm, retriever=retriver),
            )
        ]
        agent = initialize_agent(
            agent=AgentType.OPENAI_FUNCTIONS, tools=tools, llm=llm, verbose=True
        )
        agent({"input": "Who is yusuf caliskan"})
