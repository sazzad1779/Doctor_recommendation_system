from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from typing import List, Tuple
from langchain_core.documents import Document
import uuid
from dotenv import load_dotenv
from  src.dataset_normalize import load_json_file,batch_process_doctors
load_dotenv(override=True)

# Chunking setup
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    add_start_index=True,
)

# Embedding function
embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Chroma DB
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

# Load and split files (for documents like PDFs, Word, etc.)
def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.json'):
        loader = JSONLoader(file_path, jq_schema=".", text_content=False)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    documents = loader.load()
    return text_splitter.split_documents(documents)

# Index regular documents
def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        for split in splits:
            split.metadata['file_id'] = file_id
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

# Delete file-based documents
def delete_doc_from_chroma(file_id: int):
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False

# Prepare doctor-level chunked documents
def prepare_doctor_chunks(preprocessed_data: List[Tuple[str, dict]]) -> List[Document]:
    all_chunks = []
    for data in preprocessed_data:
        chunks = text_splitter.create_documents([data["text"]], metadatas=[data["metadata"]])
        all_chunks.extend(chunks)
    return all_chunks

# Index doctor data
def index_doctors_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        raw_data = load_json_file(file_path)
        preprocessed_data = batch_process_doctors(raw_data) 
        doctor_chunks = prepare_doctor_chunks(preprocessed_data)
        for chunks in doctor_chunks:
            chunks.metadata['file_id'] = file_id
        vectorstore.add_documents(doctor_chunks)
        print(f"Indexed {len(doctor_chunks)} doctor chunks.")
        return True
    except Exception as e:
        print(f"Error indexing doctor profiles: {e}")
        return False

# Delete a specific doctor by ID
def delete_doctor_from_chroma(doctor_id: str):
    try:
        vectorstore._collection.delete(where={"doctor_id": doctor_id})
        print(f"Deleted doctor with ID {doctor_id}")
        return True
    except Exception as e:
        print(f"Error deleting doctor: {e}")
        return False
