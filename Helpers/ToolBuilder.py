from Helpers.Loader import Loader
from Helpers.Textor import Textor


class ToolBuilder:
    @staticmethod
    def createToolsArray():
        files = Loader.loadedFilesInformations
        tools = []
        for file in files:
            pass

            # tools.append({"name": doc.metadata["source"], "doc": doc.page_content})
