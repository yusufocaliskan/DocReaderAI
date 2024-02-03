from DocReaderAI import DocReaderAI
from icecream import ic
from os import environ

from dotenv import load_dotenv

load_dotenv()
while True:

    print("==============================")
    question = input("Ask something...")
    answer = DocReaderAI.ask(question)
    print("==============================")
    ic(answer)
