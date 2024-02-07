from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, Field

from langchain.agents import AgentType, initialize_agent

from dotenv import load_dotenv
from langchain.globals import set_debug

load_dotenv()

set_debug(True)


class DocumentInput(BaseModel):
    question: str = Field()


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125", verbose=True)


tools = []
files = [
    {
        "name": "yusuf_caliskan",
        "path": "/Users/yusufcaliskan/GPTVerse/doc-reader/assets/files/Yusuf_Caliskan_Resume.pdf",
    },
    {
        "name": "hasan_ozkul",
        "path": "/Users/yusufcaliskan/GPTVerse/doc-reader/assets/files/hasan_ozkul.pdf",
    },
    {
        "name": "ramazan_burak_korkmaz",
        "path": "/Users/yusufcaliskan/GPTVerse/doc-reader/assets/files/RamazanBurakKorkmaz.pdf",
    },
    {
        "name": "kos_holding",
        "path": "/Users/yusufcaliskan/GPTVerse/doc-reader/assets/files/1667884932282_2202211080817467421.pdf",
    },
]


for file in files:
    loader = PyPDFLoader(file["path"])
    pages = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(pages)
    embeddings = OpenAIEmbeddings()
    retriever = FAISS.from_documents(docs, embeddings).as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 4, "score_threshold": 0.5},
    )

    # Wrap retrievers in a Tool
    tools.append(
        Tool(
            args_schema=DocumentInput,
            name=file["name"],
            description=f"useful when you want to answer questions about {file['name']}",
            func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
        )
    )


agent = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    llm=llm,
    verbose=True,
)

answer = agent({"input": "did koc holding has revenue? "})

print(answer)
