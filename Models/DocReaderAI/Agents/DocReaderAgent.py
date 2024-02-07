from typing import Optional, Type
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from langchain_core.language_models import BaseChatModel
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

# class SearchInput(BaseChatModel):
#     query: str = Field(description="should be a search query")


class DocReaderAgent(BaseTool):
    name = "doc_reader_main_agent"
    description = "usefull tools for reading documentation"
    # args_schema: Type[BaseTool] = SearchInput

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        """Dock Reader"""
        return "DocReader Runing" + query
