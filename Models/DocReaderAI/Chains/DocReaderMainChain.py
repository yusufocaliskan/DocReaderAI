from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class DocReaderMainChain:

    @staticmethod
    def instance(llm, question):
        return LLMChain(llm=llm, prompt=DocReaderMainChain.template(question))

    @staticmethod
    def template(question):
        template = PromptTemplate(
            input_variables=["question"],
            template=f"You are a philosopher, answer the question. Question is:  {question}",
        )

        return template
