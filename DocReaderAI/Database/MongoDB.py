from dotenv import load_dotenv
from pymongo import MongoClient

from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

from DocReaderAI.Helpers.Textor import Textor

load_dotenv()


class MongoDB:

    # Instance of the doc
    dbInstance: MongoClient

    # The embeddings Generator
    embedding: OpenAIEmbeddings

    # Index name of the vector search
    vectorSearchIndexName = None

    # The collection that the vectors will be stored
    collection = None

    def __init__(self) -> None:

        self.dbInstance = MongoClient("mongodb://127.0.0.1:27017/")
        self.embedding = OpenAIEmbeddings()
        self.collection = "pdfDocumentCollection"
        self.vectorSearchIndexName = "pdfDocumentIndex"

    def searchVectorFromDocument(self, docs):
        """Generates mongo db vector Collecxtion"""
        splittedDocs = Textor.splitteDocuments(docs)
        search = MongoDBAtlasVectorSearch.from_documents(
            documents=splittedDocs,
            embedding=self.embedding,
            index_name=self.vectorSearchIndexName,
            collection=self.collection,
        )
        return search
