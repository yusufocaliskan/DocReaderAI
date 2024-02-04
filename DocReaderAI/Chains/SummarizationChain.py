from langchain.chains.summarize import load_summarize_chain


class SummarizationChain:

    @staticmethod
    def summarize(llm, text, **kwargs):

        chain = load_summarize_chain(llm=llm, chain_type="map_reduce", **kwargs)
        return chain.run(text)
