import yaml
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 🔍 Load vector database
def load_db():
    return FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# 📂 Load Prompt Template
def load_prompt_template(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return PromptTemplate(
        input_variables=data.get("input_variables", []),
        template=data["template"]
    )

def run(chain_file):
    print(f"🔗 Running chain from {chain_file}...")

    # Stelle sicher, dass der Pfad zur YAML-Datei korrekt ist
    if not Path(chain_file).exists():
        print(f"❌ Error: The file '{chain_file}' does not exist.")
        return

    # Lade die Datenbank
    db = load_db()

    # Lade die YAML-Datei
    with open(chain_file, "r") as f:
        chain = yaml.safe_load(f)

    context = {}

    # Verarbeite die Schritte der Chain
    for step in chain["steps"]:
        prompt_path = Path("prompts") / step["prompt_template"]
        prompt = load_prompt_template(prompt_path)  # Lade das Prompt Template

        if step.get("ask_user", False):
            # Eingabeaufforderung nur für Variablen, die benötigt werden und nicht durch die Datenbank bereitgestellt werden
            for var in prompt.input_variables:
                if var != "research":  # Verhindere, dass nach 'research' gefragt wird
                    user_input = input(f"Input for '{var}': ")
                    context[var] = user_input

        if step.get("use_vector_search", False):
            query = context.get("description", "")
            result = db.similarity_search(query, k=2)  # Führe eine Ähnlichkeitssuche in der DB durch
            context["research"] = "\n".join([d.page_content for d in result])  # Fülle 'research' mit den Suchergebnissen

        filled_prompt = prompt.format(**context)  # Fülle das Template mit den Kontextinformationen
        result = ChatOpenAI(temperature=0, model_name="gpt-4").predict(filled_prompt)  # Hole die Antwort vom LLM
        context[step["id"]] = result

        print(f"\n🔹 Step '{step['id']}':\n{result}\n")
