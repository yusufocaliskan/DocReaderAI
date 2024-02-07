from icecream import ic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

from langchain.retrievers import EnsembleRetriever
from langchain_openai import ChatOpenAI

from .Textor import Textor


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125", verbose=True)


# To load some docs
class Loader:

    loadedFiles = []
    loadedFilesInformations = []

    # Retuns length of the loaded files
    @staticmethod
    def getLenghtOfLoadedFiles():
        return len(Loader.loadedFiles)

    # just for debuggin
    # print(str(Loader))
    def __str__(self):
        ic(Loader.loadedFiles)
        return ""

    @staticmethod
    def combineLoadedFilesAsEnsembleRetrieverStore():
        ## search_type="similarity_score_threshold" to get scores
        files = Loader.loadedFiles
        retrievers = []
        weights = []
        for file in files:
            docVS = Textor.transform2Vectors(file)
            doc2Retriever = docVS.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 2, "score_threshold": 0.5},
            )
            retrievers.append(doc2Retriever)
            weights.append(0.5)

        compiledEssambleRetriever = EnsembleRetriever(
            retrievers=retrievers,
            weights=weights,
        )
        return compiledEssambleRetriever

    @staticmethod
    def combineLoadedFilesWidthInfo():
        files = Loader.loadedFilesInformations
        pages = []
        for file in files:
            for page in file["content"]:
                pages.append(page)

        return pages

    @staticmethod
    def combineAllLoadedFiles():
        files = Loader.loadedFiles
        pages = []
        for file in files:
            for page in file:
                pages.append(page)

        return pages

        # Load PDF

    @staticmethod
    def loadPdfFile(url):
        # Summarize the file when loaded. An save it
        # put it to the database
        loader = PyPDFLoader(url)

        loadedFile = loader.load()
        Loader.loadedFiles.append(loadedFile)
        return loadedFile

    @staticmethod
    def loadPdfFileWidthInfo(url):
        # Summarize the file when loaded. An save it
        # put it to the database
        loader = PyPDFLoader(url)

        file = loader.load()

        # Send firs page and get an meaning full name
        name = Loader.createMeaninfullNames(file)

        # Generate name for files
        Loader.loadedFilesInformations.append({"content": file, "name": name["text"]})

    @staticmethod
    def createMeaninfullNames(content):

        template = "Create a meaningfull file name base on the content, output must be like this: example_file_name Only produce one single line and name. Content is: {content}"
        prompt_template = PromptTemplate(input_variables=["content"], template=template)
        chain = LLMChain(llm=llm, prompt=prompt_template)
        resp = chain.invoke({"content": content[0]})

        return resp

    # Load web base doc {a web page, for instance}
    @staticmethod
    def loadWebBaseDoc(url):
        loader = WebBaseLoader(url)
        loadedFile = loader.load()
        Loader.loadedFiles.append(loadedFile)
        return loadedFile
