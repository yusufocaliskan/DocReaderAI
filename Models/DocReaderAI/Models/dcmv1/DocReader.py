from langchain.agents import Tool
from langchain.chains import LLMChain, RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, Field

from langchain.agents import AgentType, initialize_agent

from langchain.chains import SimpleSequentialChain

from dotenv import load_dotenv
from langchain.globals import set_debug

from Helpers.Loader import Loader
from Helpers.Textor import Textor
from Helpers.ToolBuilder import ToolBuilder

load_dotenv()
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125", verbose=True)


class DocumentInput(BaseModel):
    question: str = Field()


class DocReader:

    def run(self, question):

        tools = []

        # Get all loded raw file
        for file in Loader.loadedFilesInformations:

            # Put in a store
            store = Textor.transform2Vectors(file["content"])
            retriever = store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 4, "score_threshold": 0.5},
            )

            # CCreate an agent toos
            tools.append(
                Tool(
                    args_schema=DocumentInput,
                    name=file["name"],
                    description=f"useful when you want to answer questions about {file['name']}",
                    func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
                )
            )
        # Run the agent
        agent = initialize_agent(
            agent=AgentType.OPENAI_FUNCTIONS,
            tools=tools,
            llm=llm,
            verbose=True,
        )

        chain = SimpleSequentialChain(chains=[agent])
        # answer = agent({"input": question})
        answer = chain.run(question)
        return answer
