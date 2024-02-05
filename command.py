from DocReaderAI.Helpers.Loader import Loader
from DocReaderAI import DocReaderAI
from icecream import ic
from dotenv import load_dotenv

load_dotenv()
chat_history = []
Loader.loadPdfFile("assets/files/hasan_ozkul.pdf")
Loader.loadPdfFile("assets/files/RamazanBurakKorkmaz.pdf")
Loader.loadPdfFile("assets/files/Yusuf_Caliskan_Resume.pdf")


while True:

    print("==============================")
    question = input("Ask something: ")
    answer = DocReaderAI().askType5(question=question, chat_history=chat_history)

    print("==============================")

    chat_history.append({"q": question, "a": answer})
    print(answer)
