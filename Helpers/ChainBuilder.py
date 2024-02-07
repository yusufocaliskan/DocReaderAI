from langchain.chains import LLMChain, SimpleSequentialChain


class ChainBuilder:
    """Utility class to produces  new chain instances"""

    listOfChains = []

    # Creates new chain
    @staticmethod
    def create(**kwargs):
        chain = LLMChain(**kwargs)
        ChainBuilder.listOfChains.append(chain)
        return chain

    @staticmethod
    def sequential(**kwargs):
        return SimpleSequentialChain(**kwargs)
