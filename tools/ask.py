from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings

# 🔍 Load vector database
def load_db():
    return FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

def run():
    print("🧠 Ask a question...")

    query = input("Question: ")

    db = load_db()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    response = qa_chain.run(query)

    print("\nAnswer:\n")
    print(response)

