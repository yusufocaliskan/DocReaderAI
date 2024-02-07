from icecream import ic
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

from langchain.retrievers import EnsembleRetriever

from .Textor import Textor


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
    def loadPdfFileWidthInfo(url, name):
        # Summarize the file when loaded. An save it
        # put it to the database
        loader = PyPDFLoader(url)

        file = loader.load()
        Loader.loadedFilesInformations.append({"content": file, "name": name})

    # Load web base doc {a web page, for instance}
    @staticmethod
    def loadWebBaseDoc(url):
        loader = WebBaseLoader(url)
        loadedFile = loader.load()
        Loader.loadedFiles.append(loadedFile)
        return loadedFile
