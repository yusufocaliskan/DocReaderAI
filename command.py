from Helpers.Loader import Loader
from Models.DocReaderAI import DocReaderAI
from icecream import ic
from dotenv import load_dotenv

load_dotenv()
chat_history = []

Loader.loadPdfFileWidthInfo(
    url="assets/files/Yusuf_Caliskan_Resume.pdf", name="yusuf_caliskan"
)
Loader.loadPdfFileWidthInfo(url="assets/files/hasan_ozkul.pdf", name="hasan_ozkul")
Loader.loadPdfFileWidthInfo(
    url="assets/files/RamazanBurakKorkmaz.pdf", name="ramazan_burak_korkmaz"
)


while True:

    print("==============================")
    question = input("Ask something: ")
    print("==============================")
    AI = DocReaderAI()
    answer = AI.ask(question=question, chat_history=chat_history)

    chat_history.append({"q": question, "a": answer})
    print(answer)
