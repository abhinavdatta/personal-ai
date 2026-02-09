import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import torch


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def ingest_pdfs(pdf_dir="data/pdfs", out="embeddings"):
    documents = []

    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_dir, file))
            pages = loader.load()
            documents.extend(pages)

    if not documents:
        raise RuntimeError("No readable PDFs found")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": get_device()}
    )

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(out)

    print("✅ PDF ingestion complete. Embeddings updated.")
