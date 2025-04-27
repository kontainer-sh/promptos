from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.docstore.document import Document
import glob

def run():
    print("🔨 Building index...")

    # 🏗 Build index from Markdown files
    documents = []
    for filepath in glob.glob("./docs/*.md"):
        with open(filepath, 'r') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": filepath}))

    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    db.save_local("faiss_index")
    print("✅ Index successfully built and saved.")

