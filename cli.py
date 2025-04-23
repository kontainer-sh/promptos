import argparse
import os
import yaml
import glob
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.docstore.document import Document

# 📦 Setup
load_dotenv()
llm = ChatOpenAI(temperature=0, model_name="gpt-4")

# 📂 Prompt Template laden
def load_prompt_template(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return PromptTemplate(
        input_variables=data.get("input_variables", []),
        template=data["template"]
    )

# 🔍 Vektor-Datenbank laden
def load_db():
    return FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# 🏗 Index aufbauen aus Markdown-Dateien
def build_index():
    documents = []
    for filepath in glob.glob("./docs/*.md"):
        with open(filepath, 'r') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": filepath}))

    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    db.save_local("faiss_index")
    print("✅ Index erfolgreich gebaut und gespeichert.")

# 💬 Einzelne Frage beantworten mit Vektor-Unterstützung
def run_prompt(query):
    db = load_db()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    response = qa_chain.run(query)
    print("\nAntwort:\n")
    print(response)

# 🔗 Chain Runner
def run_chain(chain_file):
    db = load_db()
    with open(chain_file, "r") as f:
        chain = yaml.safe_load(f)

    context = {}

    for step in chain["steps"]:
        prompt_path = Path("prompts") / step["prompt_template"]
        prompt = load_prompt_template(prompt_path)

        if step.get("ask_user", False):
            for var in prompt.input_variables:
                user_input = input(f"Eingabe für '{var}': ")
                context[var] = user_input

        if step.get("use_vector_search", False):
            query = context.get("beschreibung", "")
            result = db.similarity_search(query, k=2)
            context["recherche"] = "\n".join([d.page_content for d in result])

        filled_prompt = prompt.format(**context)
        result = llm.predict(filled_prompt)
        context[step["id"]] = result

        print(f"\n🔹 Schritt '{step['id']}':\n{result}\n")

# 🖥️ CLI Setup
parser = argparse.ArgumentParser(description="🧠 Consulting Assistant CLI")
parser.add_argument("command", choices=["build-index", "ask", "run-chain"], help="Aktion auswählen")
parser.add_argument("arg", nargs="?", help="Frage oder Pfad zur Chain-Datei")

args = parser.parse_args()

# 🔧 Routing
if args.command == "build-index":
    build_index()

elif args.command == "ask":
    if not args.arg:
        args.arg = input("Frage: ")
    run_prompt(args.arg)

elif args.command == "run-chain":
    if not args.arg:
        args.arg = input("Pfad zur Chain (z. B. chains/xxx.yaml): ")
    run_chain(args.arg)

