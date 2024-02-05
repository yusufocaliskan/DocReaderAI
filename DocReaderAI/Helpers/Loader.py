from icecream import ic
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader


# To load some docs
class Loader:

    loadedFiles = []

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

    # Load web base doc {a web page, for instance}
    @staticmethod
    def loadWebBaseDoc(url):
        loader = WebBaseLoader(url)
        loadedFile = loader.load()
        Loader.loadedFiles.append(loadedFile)
        return loadedFile
