import boto3
import chromadb
import json
from langchain_core.documents import Document
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

from utils.settings import PATH_TO_CHROMA_DB


class KnowledgeBase:

    def __init__(
        self,
        collection_name: str,
        embedding_model_name: str = "amazon.titan-embed-text-v1",
        chunk_size: int = 1_000,
        chunk_overlap: int = 200,
    ) -> None:
        self.embedding_model_name = embedding_model_name

        self.chroma_client =chromadb.PersistentClient(
            path=PATH_TO_CHROMA_DB,
        )
        if collection_name in self.chroma_client.list_collections():
            self.chroma_client.delete_collection(collection_name)
        self.collection = self.chroma_client.get_or_create_collection(
            collection_name,
        )

        self.client = boto3.client("bedrock-runtime")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        )

    def _get_embeddings(self, text: str) -> list[float]:
        response = self.client.invoke_model(
            modelId=self.embedding_model_name,
            body=json.dumps({"inputText": text}),
        )
        embedding_output = json.loads(response["body"].read())
        return embedding_output["embeddings"]
    
    def _load_pdf(self, file_path: Path) -> list[Document]:
        loader = PDFPlumberLoader(file_path)
        return loader.load()
    
    def _split_text(self, documents: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(documents)
    
    def update(self, file_path: Path) -> None:
        prefix = file_path.stem
        chunked_documents: list[Document] = self._split_text(
            self._load_pdf(file_path)
        )
        doc_ids = [f"{prefix}_{idx+1}" for idx in range(len(chunked_documents))]
        texts = [p.page_content for p in chunked_documents]
        embeddings = [self._get_embeddings(text) for text in texts]
        self.collection.add(
            ids=doc_ids,
            documents=texts,
            embeddings=embeddings,
        )

    def retrieve(self, query: str, top_k: int = 2) -> str:
        response = self.collection.query(
            query_embeddings=self._get_embeddings(query),
            n_results=top_k,
        )
        return "\n".join(response["documents"][0])
