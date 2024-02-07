from Helpers.Loader import Loader
from Models.DocReaderAI import DocReaderAI
from icecream import ic
from dotenv import load_dotenv

load_dotenv()
chat_history = []

Loader.loadPdfFileWidthInfo(url="assets/files/Yusuf_Caliskan_Resume.pdf")
Loader.loadPdfFileWidthInfo(url="assets/files/hasan_ozkul.pdf")
Loader.loadPdfFileWidthInfo(url="assets/files/RamazanBurakKorkmaz.pdf")
Loader.loadPdfFileWidthInfo(url="assets/files/1667884932282_2202211080817467421.pdf")

while True:

    print("==============================")
    question = input("Ask something: ")
    print("==============================")
    AI = DocReaderAI()
    answer = AI.ask(question=question, chat_history=chat_history)

    chat_history.append({"q": question, "a": answer})
    print(answer)
