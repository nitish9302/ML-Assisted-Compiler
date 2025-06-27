# 📝 ML - Assisted Compiler Complete Technical Documentation

## 📌 Overview

**Machine Learning Assisted Compiler** is a full-featured desktop-based development environment designed to simplify the creation and debugging of **Lex (Flex)** lexical analyzer programs. It combines a friendly graphical interface with real-time compilation, stdin input handling, and a smart error suggestion system powered by both **machine learning (ML)** and **OpenAI's GPT** models.

It is an educational and productivity tool tailored for:

- Compiler design students
- Academic use in C/Lex environments
- Developers prototyping scanners or learning compiler theory

---

## 🧱 Project Structure

```
LexIDE/
├── frontend/
│   └── gui.py                  # GUI interface built using Tkinter
├── core/
│   ├── runner.py              # Compiles & executes user-submitted Lex code
│   └── utils.py               # Temp path and directory utilities
├── ml/
│   └── suggestion_engine.py   # ML + GPT based error suggestion engine
├── temp/                      # Temporary workspace (code and output)
├── main.py                    # Entry point to run the IDE

```

---

## 🧰 Requirements and Installation

### 🐍 Python Modules

Install all required Python packages using pip:

```bash
pip install sentence-transformers numpy scikit-learn openai

```

### 🧾 External Dependencies (System-level)

Ensure the following are installed and added to your system PATH:

- `flex` (Lex compiler)
- `gcc` (GNU C Compiler)

### 🔧 On Linux/macOS:

```bash
sudo apt install flex gcc          # Debian/Ubuntu

```

### 🔧 On Windows:

- Use MinGW or TDM-GCC
- Install Flex via Cygwin or Windows Subsystem for Linux (WSL)
- Add both tools to environment variables

---

## 🖥️ Feature Overview

### ✍️ 1. Code Editor

- Full Lex code editor using Tkinter’s `ScrolledText`
- Allows writing `.l` files directly inside the GUI

### 🔽 2. Input Box

- Accepts stdin input (like `scanf` input to `yylex()`)
- Shows user prompt simulation

### 📤 3. Output Panel

- Displays final stdout, errors, and suggestions
- Styled with read-only scrollable text

### 🧠 4. Smart Error Fix Suggestions

- Uses `MiniLM` sentence embeddings for semantic similarity
- Compares compiler output to a known error database
- If no high-match score, calls GPT-3.5 via OpenAI API for help

### ⚙️ 5. One-Click Compilation

- Executes this process in a background thread:
    1. Save code to `temp/user_code.l`
    2. Run `flex` to generate `lex.yy.c`
    3. Compile `lex.yy.c` with `gcc` to `output.exe`
    4. Execute it and feed user input via `stdin`

### 📂 6. Temporary File Safety

- All code, output, and build files are stored in the `/temp/` folder
- Keeps workspace clean and prevents overwriting user code

---

## ⚙️ Internal Module Logic

### 🔹 `runner.py`

- Handles:
    - Writing Lex code to disk
    - Running `flex` → generates `lex.yy.c`
    - Compiling with `gcc`
    - Executing the compiled binary using `subprocess.run()`
    - Capturing stdout and stderr output
    - Returning execution results

### 🔹 `suggestion_engine.py`

- Loads a curated list of known Lex/C error patterns
- Converts all errors to embeddings using `MiniLM`
- On error:
    - Matches the user error with known embeddings
    - If cosine similarity > 0.5 → returns best fix
    - Else → uses OpenAI GPT (if key is present) to generate fix

### 🔹 `gui.py`

- Tkinter-based user interface
- Handles file open/save, code editing, input/output rendering
- Manages background threads to avoid UI freezing
- Integrates output parsing to smartly strip redundant prompts
- Displays suggestions intelligently next to error messages

---

## 🧪 Example Usage Flow

1. Launch the app with `python main.py`
2. Write or paste a Lex `.l` program (e.g., identifier validator)
3. Click **Run**
4. Enter input when prompted (e.g. `var1`, `1abc`, etc.)
5. View the output or error
6. If an error is detected:
    - LexIDE will suggest a fix based on known errors
    - If not found, GPT-3.5 will provide a natural-language fix

---

## 🔐 GPT Fallback (Optional)

To use GPT for unknown error suggestion:

1. Get your OpenAI API key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Set the key as an environment variable:
    
    ```bash
    export OPENAI_API_KEY=your-key    # Linux/macOS
    set OPENAI_API_KEY=your-key       # Windows
    
    ```
    
3. Or modify `suggestion_engine.py` to set the key directly *(not recommended for security)*

---

## ✅ Summary

LexIDE provides:

- 🔧 Simple but powerful Lex development UI
- 🚀 One-click build + run pipeline using `flex` and `gcc`
- 🤖 Intelligent ML and AI suggestions for compiler errors
- 🎓 An ideal platform for learning compiler design interactively

It replaces the need for complex CLI commands and helps understand error patterns quickly.

---

## 🌱 Potential Future Enhancements

- [ ]  Lex/Yacc integrated mode with `.y` file handling
- [ ]  Code syntax highlighting in editor
- [ ]  Embedded terminal for real-time I/O behavior
- [ ]  Export logs, output, and debugging history
- [ ]  AI-trained suggestion models from large C error corpora
- [ ]  Toggle between GPT/local modes from UI

---
