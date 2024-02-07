# Helpers
from dotenv import load_dotenv
from os import environ
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import tool
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import EnsembleRetriever

# Langchain
from langchain_openai import OpenAI
from langchain import hub

# agent
from langchain.agents import (
    AgentExecutor,
    AgentType,
    create_openai_functions_agent,
    initialize_agent,
    load_tools,
)
from .Agents.DocReaderAgent import DocReaderAgent

# DocReaderAI
from Helpers.Loader import Loader
from Helpers.ChainBuilder import ChainBuilder
from .Agents.AgentBuilder import AgentBuilder
from Helpers.Templator import Templator
from Database.FaissDB import FaissDB
from Helpers.Debug import Debug
from .Templates.TemplatesHolder import TemplatesHolder
from Helpers.Textor import Textor
from .Models.dcmv1.DocReader import DocReader


load_dotenv()
OPENAI_TEMPERATURE = environ.get("OPENAI_TEMPERATURE")
llm = OpenAI(temperature=OPENAI_TEMPERATURE)


class DocReaderAI:

    fd: FaissDB

    vectorDBInstance = None

    def __init__(self) -> None:
        combinedFiles = Loader.combineAllLoadedFiles()
        self.fd = FaissDB()
        self.vectorDBInstance = self.fd.createDBFromDocument(docs=combinedFiles)

    def ask10(self, question, chat_history):
        DocReader().run(question)

    def ask9(self, question, chat_history):
        loadedFiles = Loader.loadedFiles
        AgentBuilder.build(loadedFiles=loadedFiles)

    # Techneque -1
    # Does't give meaningful feed back
    def ask8(self, question, chat_history):
        store = Loader.combineLoadedFilesAsEnsembleRetrieverStore()

        docs = store.invoke(question)
        docs2Text = Textor.convertDocs2Text(docs)
        prompt = Templator.prompt(
            input_variables=["question", "docs", "chat_history"],
            template=TemplatesHolder.mainDocReaderTemplate,
        )

        chain = ChainBuilder.create(llm=llm, prompt=prompt, verbose=True)
        resp = chain.run(question=question, docs=docs2Text, chat_history=chat_history)

        return resp

    def ask7(self, question):
        result = DocReaderAgent()
        print(result.run("Selamm"))

    def ask4(self, question):
        tools = load_tools(["wikipedia"])
        memory = ConversationBufferMemory()
        agent = initialize_agent(
            tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
        agent.run(question)

    def ask3(self, question):
        retriever = self.vectorDBInstance.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.5},
            k=2,
        )
        docs = retriever.get_relevant_documents(question)

        prompt = Templator.prompt(
            input_variables=["question", "docs", "chat_history"],
            template=TemplatesHolder.mainDocReaderTemplate,
        )

        docReaderChain = ChainBuilder.create(llm=llm, prompt=prompt, verbose=True)
        content = " ".join([doc.page_content for doc in docs])

        conenteSummarizePrompt = Templator.prompt(
            input_variables=["docs"],
            template=TemplatesHolder.summarizTextTemplate,
        )

        summarizor = ChainBuilder.create(
            llm=llm, prompt=conenteSummarizePrompt, verbose=True
        )
        squentialChain = SimpleSequentialChain(chains=[summarizor, docReaderChain])

        # resp = SummarizationChain.summarize(llm=llm, text=content)
        # return resp
        asnwer = squentialChain.run(question)

        return asnwer

    # @staticmethod
    # def ask(question, k=4):
    #
    #     # Load the raw content from the given files
    #     combinedFiles = Loader.combineAllLoadedFiles()
    #     allStoreDoc = Textor.transform2Vectors(combinedFiles)
    #     queryResult = allStoreDoc.similarity_search(question, k)
    #     print("queryResult-->", queryResult)
    #
    #     # Combine them
    #     content = " ".join([doc.page_content for doc in queryResult])
    #
    #     prompt = PromptTemplate(
    #         input_variables=["question", "docs"],
    #         template="""
    #             Use maximum of 150 words to answer my question.
    #             Your answer must only in the context of the question. Do add any more information is the human doesn't needed.
    #             Also answer with same language User using in the question
    #             Use the following pieces of context and try your best to answer user question.
    #             If data is tabular, analyze data as tabular data not text or pdf.
    #             <context>
    #             {docs}
    #             <context>
    #             My question is: {question}
    #         """,
    #     )
    #
    #     # conversation = ConversationChain(llm=llm, prompt=prompt)
    #
    #     chain = LLMChain(llm=llm, prompt=prompt)
    #     answer = chain.run(question=question, docs=content)
    #     return answer

    def ask(self, question):

        # retrieverTool = create_retriever_tool(
        #     self.askDocumentChain,
        #     "DocReader",
        #     "use it when you asked for document informations",
        # )
        # prompt = PromptTemplate(
        #     input_variables=["question"],
        #     template="You are an author, answer this: {question}",
        # )
        prompt = hub.pull("hwchase17/openai-functions-agent")
        essay = LLMChain(llm=llm, prompt=prompt, verbose=True)
        # print(essay.run(input=question))

        tools = [
            Tool(
                name="Essay",
                func=essay.run,
                description="use it when you need to create an essay",
            )
        ]
        agent = initialize_agent(
            tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
        )

        agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        print(agentExecutor.invoke({"input": "Write an essay about how to codding"}))

        return
        # self.askDocumentChain(question, chat_history)
        agent = initialize_agent(tools, llm=llm, agent=AgentType.OPENAI_FUNCTIONS)
        agent.run()

    def searchTool(self):
        """To search somethig..."""
        return "Searchinnnnnnnnnn...."

    def ask2(question):
        combinedFiles = Loader.combineAllLoadedFiles()
        fd = FaissDB()
        vectorDBInstance = fd.createDBFromDocument(docs=combinedFiles)
        retriever = vectorDBInstance.as_retriever()

        # print(retriever.invoke("yusuf caliskan"))
        search = DuckDuckGoSearchRun()
        # print(search.invoke("who is yusuf caliskan"))
        retriever_tool = create_retriever_tool(
            retriever, "doc_search", "use when need to search document"
        )
        tools = [search]
        prompt = hub.pull("hwchase17/openai-functions-agent")
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        agent_executor.invoke({"input": "hi!"})

    def askDocumentChain(self, question, chat_history):
        """Reading Documents and answering"""
        retriever = self.vectorDBInstance.as_retriever()
        docs = retriever.get_relevant_documents(question, k=3)
        content = " ".join([doc.page_content for doc in docs])

        prompt = Templator.prompt(
            input_variables=["question", "docs", "chat_history"],
            template=mainDocReaderPromptTemplate,
        )

        chain = ChainBuilder.create(llm=llm, prompt=prompt, verbose=True)

        answer = chain.run(question=question, docs=content, chat_history=chat_history)

        return answer
