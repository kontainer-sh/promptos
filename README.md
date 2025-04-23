# 🧠 Consulting Assistant CLI

A modular and extensible AI-powered assistant designed for consultants, coaches, and creators. Build your own vector-based knowledge assistant, execute prompt workflows via YAML-defined chains, and automate responses using GPT-4 and LangChain.

## ✨ Features

- 📚 Create a semantic knowledge base from Markdown files using vector search.
- 🔗 Execute multi-step workflows defined as YAML chains.
- 💬 Ask GPT-4 contextual questions using vector-augmented prompts.
- 📁 Modular prompts and templates for reusability.
- ⚙️ Runs from the command line for easy integration and automation.

---

## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/consulting-assistant.git
cd consulting-assistant
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up `.env`

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

---

## 🛠️ CLI Usage

### Build the Vector Index

```bash
python cli.py build-index
```

### Ask a Question

```bash
python cli.py ask "What is the difference between strategy A and B?"
```

### Run a Multi-Step Prompt Chain

```bash
python cli.py run-chain chains/example.yaml
```

---

## 📁 Project Structure

```
consulting-assistant/
├── cli.py                # Main CLI entry point
├── docs/                 # Markdown files to be indexed
├── chains/               # YAML workflow chains
├── prompts/              # YAML prompt templates
├── .env                  # API key (not included in repo)
├── requirements.txt      # Python dependencies
└── faiss_index/          # Saved vector database (generated)
```

---

## 📄 Example Prompt Template (`prompts/idea.yaml`)

```yaml
input_variables:
  - beschreibung
  - recherche
template: |
  Based on the following user description and research, suggest 3 product ideas:

  Description:
  {beschreibung}

  Research:
  {recherche}
```

---

## 🧠 Example Chain (`chains/idea-generator.yaml`)

```yaml
steps:
  - id: idea_suggestion
    prompt_template: idea.yaml
    ask_user: true
    use_vector_search: true
```

---

## 💡 Future Ideas

- Add support for exporting results (Markdown, PDF, Word).
- Integrate agent-based decision trees (LangGraph or CrewAI).
- Build a marketplace for reusable prompts and chains.
- Wrap in a GUI for non-technical users.

---

## 📖 License

MIT License — use, modify, and build upon freely.