# Helpers
from icecream import ic
from dotenv import load_dotenv
from os import environ

# Langchain
from langchain.chains import ConversationChain, LLMChain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain

# agent
from langchain.agents import tool, load_tools, initialize_agent

# DocReaderAI
from DocReaderAI.Helpers.Loader import Loader
from DocReaderAI.Helpers.Textor import Textor
from DocReaderAI.Chains.SummarizationChain import SummarizationChain
from DocReaderAI.Helpers.ChainBuilder import ChainBuilder
from DocReaderAI.Helpers.Templator import Templator
from DocReaderAI.Database.FaissDB import FaissDB

from DocReaderAI.Templates.mainDocReaderPromptTemplate import (
    mainDocReaderPromptTemplate,
)


load_dotenv()
OPENAI_TEMPERATURE = environ.get("OPENAI_TEMPERATURE")
llm = OpenAI(temperature=OPENAI_TEMPERATURE)


class DocReaderAI:

    fd: FaissDB

    def __init__(self) -> None:
        combinedFiles = Loader.combineAllLoadedFiles()
        self.fd = FaissDB(docs=combinedFiles)

    @staticmethod
    def ask(question, k=4):

        # Load the raw content from the given files
        combinedFiles = Loader.combineAllLoadedFiles()
        allStoreDoc = Textor.transform2Vectors(combinedFiles)
        queryResult = allStoreDoc.similarity_search(question, k)
        print("queryResult-->", queryResult)

        # Combine them
        content = " ".join([doc.page_content for doc in queryResult])

        prompt = PromptTemplate(
            input_variables=["question", "docs"],
            template="""
                Use maximum of 150 words to answer my question.
                Your answer must only in the context of the question. Do add any more information is the human doesn't needed. 
                Also answer with same language User using in the question
                Use the following pieces of context and try your best to answer user question.
                If data is tabular, analyze data as tabular data not text or pdf.
                <context>
                {docs}
                <context>
                My question is: {question}
            """,
        )

        # conversation = ConversationChain(llm=llm, prompt=prompt)

        chain = LLMChain(llm=llm, prompt=prompt)
        answer = chain.run(question=question, docs=content)
        return answer

    @staticmethod
    def askType2(question, chat_history, k=1):

        # Load the raw content from the given files
        combinedFiles = Loader.combineAllLoadedFiles()
        allStoreDoc = Textor.transform2Vectors(combinedFiles)
        queryResult = allStoreDoc.similarity_search(question, k)
        print("queryResult-->", queryResult)

        # Combine them
        content = " ".join([doc.page_content for doc in queryResult])

        # Create a prompt
        prompt = ChatPromptTemplate.from_template(
            """
                Use maximum of 150 words to answer my question.
                Your answer must only in the context of the question. Do add any more information is the human doesn't needed. 
                Also answer with same language User using in the question
                Use the following pieces of context and try your best to answer user question.
                If data is tabular, analyze data as tabular data not text or pdf.
                If you don't have any idea about the question, simple say : I dont't know. And don't produce informations.
                If you need more information, ask for more information.

                <context>
                {context}
                <context>
                My question is: {question}
            """,
        )

        # ask to the Model to give a answer in the context of the given data
        chain = create_stuff_documents_chain(llm, prompt)
        answer = chain.invoke(
            {"question": question, "context": [Document(page_content=content)]}
        )

        # simple retun the answer
        return answer

    def askType5(self, question, chat_history):

        # queryResult = db.similarity_search(question, k=3)
        vectorizedQuery = self.fd.embbedingTextQuery(text=question)
        queryResult = self.fd.vectorDBInstance.similarity_search_with_score(
            question, k=3
        )
        # print("self.fd.vectorDBInstance", self.fd.vectorDBInstance)
        # queryResult = self.fd.vectorDBInstance.similarity_search_by_vector(
        #     vectorizedQuery, k=3
        # )
        retriever = self.fd.vectorDBInstance.as_retriever()

        # docs = retriever.invoke(question)

        ic("Result: -->", queryResult)

    @staticmethod
    def askType3(question, chat_history):

        # Load the raw content from the given files
        combinedFiles = Loader.combineAllLoadedFiles()

        # Summarize text
        # summarizedText = SummarizationChain.summarize(
        #     llm=llm, text=combinedFiles, verbose=True
        # )

        # splittedText = Loader.splitteText(summarizedText)

        historical_context = " "
        for ch in chat_history:
            historical_context += f"question: {ch['q']}. \n answer: {ch['a']} \n"

        allStoreDoc = Textor.transform2Vectors(combinedFiles)

        ## produce getLenghtOfLoadedFiles amon
        k = Loader.getLenghtOfLoadedFiles()
        queryResult = allStoreDoc.similarity_search(question, k)

        # Combine them
        content = " ".join([doc.page_content for doc in queryResult])

        # memory = ConversationBufferMemory(memory_key="chat_history")

        # Create a prompt
        prompt = Templator.prompt(
            input_variables=["question", "docs", "chat_history"],
            template=mainDocReaderPromptTemplate,
        )
        chain = ChainBuilder.create(llm=llm, prompt=prompt, verbose=True)

        answer = chain.run(
            question=question, docs=content, chat_history=historical_context
        )

        return answer

    @tool
    def lenOfSring(name: str) -> int:
        """Returns the length of a word."""
        return len(name)

    @staticmethod
    def askType4(question):
        return DocReaderAI.askType3.invoke(question, verbose=True)
