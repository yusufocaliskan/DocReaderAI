# DocReaderAI
from .Models.dcmv1.DocReader import DocReader


# load_dotenv()
# OPENAI_TEMPERATURE = environ.get("OPENAI_TEMPERATURE")
#


class DocReaderAI:

    def ask(self, question, chat_history):
        return DocReader().run(question)
