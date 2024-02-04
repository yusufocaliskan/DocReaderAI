from DocReaderAI.DocLoader.Loader import Loader
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
    question = input("Ask something...")
    answer = DocReaderAI.askType2(question, chat_history)
    print("==============================")
    chat_history.append(answer)
    print(answer)
