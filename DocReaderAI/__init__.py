from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from os import environ
from DocReaderAI.DocLoader.Loader import Loader


load_dotenv()
OPENAI_TEMPERATURE = environ.get("OPENAI_TEMPERATURE")
llm = OpenAI(temperature=OPENAI_TEMPERATURE, streaming=True)


class DocReaderAI:

    @staticmethod
    def ask(question, k=4):

        docRaw = Loader.loadPdfFile("assets/files/hasan_ozkul.pdf")
        savedVectoralData = Loader.transform2Vectors(docRaw).similarity_search(
            question, k
        )

        content = " ".join([doc.page_content for doc in savedVectoralData])
        prompt = PromptTemplate(
            input_variables=["question", "docs"],
            template="""
                Use maximum of 150 words to answer my question.
               Your answer must only in the context of the question. Do add any more information is the human doesn't needed. 
                Also answer with same language User using in the question
                Use the following pieces of context and try your best to answer user question.
                If data is tabular, analyze data as tabular data not text or pdf.
                My question is: {question}
            """,
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        answer = chain.run(question=question, docs=content)
        return answer
