import torch
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

DEVICE = get_device()

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL,
    model_kwargs={"device": DEVICE}
)

def load_store(path="embeddings"):
    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )
