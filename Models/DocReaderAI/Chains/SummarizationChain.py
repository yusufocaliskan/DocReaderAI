from langchain.chains.summarize import load_summarize_chain


class SummarizationChain:

    @staticmethod
    def summarize(llm, text, **kwargs):

        # map_reduce = Summarization of the Summarization
        chain = load_summarize_chain(llm=llm, chain_type="map_reduce", **kwargs)
        resp = chain.run(text)
        return resp
