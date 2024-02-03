from dotenv import load_dotenv
from langchain_openai import OpenAI
from icecream import ic
from os import environ
from src.Chains.DocReaderMainChain import DocReaderMainChain
from src.DocLoader.Loader import Loader

load_dotenv()
OPENAI_TEMPERATURE = environ.get("OPENAI_TEMPERATURE")
llm = OpenAI(temperature=OPENAI_TEMPERATURE)

doc = Loader("./test-pdfs/hasan_ozkul.pdf").doc
print(doc)


def askQuestion(question):

    input_chain = DocReaderMainChain.instance(llm, question)
    resp = input_chain({"question": question})

    return resp


# answer = askQuestion("Who you are?")
# if __name__ == "__main__":
# ic(answer)
