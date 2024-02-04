from langchain.prompts import PromptTemplate


class Templator:

    @staticmethod
    def prompt(**kwargs):
        return PromptTemplate(**kwargs)
