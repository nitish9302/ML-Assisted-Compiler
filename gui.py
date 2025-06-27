import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading


class LexIDE:
    def __init__(self, root, runner, suggestor):
        self.root = root
        self.runner = runner
        self.suggestor = suggestor

        self.root.title("Lex IDE")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")
        self._setup_ui()

    def _setup_ui(self):
        self._setup_toolbar()
        self._setup_panes()
        self._setup_menu()

    def _setup_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#2d2d30", height=40)
        toolbar.pack(side="top", fill="x")

        self.run_button = tk.Button(toolbar, text="▶ Run", command=self.on_run,
            bg="#007acc", fg="white", relief="flat", font=("Segoe UI", 10, "bold"),
            activebackground="#005f99", cursor="hand2")
        self.run_button.pack(side="left", padx=10)

    def _setup_panes(self):
        pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        pane.pack(fill="both", expand=True)

        left = tk.Frame(pane, bg="#1e1e1e")
        right = tk.Frame(pane, bg="#1e1e1e")

        # Code Editor
        tk.Label(left, text="Lex Code", fg="white", bg="#1e1e1e").pack(anchor="w")
        self.editor = ScrolledText(left, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4",
                                   insertbackground="white", wrap="none")
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)

        # Input Box
        tk.Label(right, text="Program Input (stdin)", fg="white", bg="#1e1e1e").pack(anchor="w")
        self.input_box = ScrolledText(right, height=5, font=("Consolas", 11),
                                      bg="#252526", fg="#d4d4d4", insertbackground="white")
        self.input_box.pack(fill="x", padx=5, pady=(0, 10))

        # Output Panel
        tk.Label(right, text="Output / Errors", fg="white", bg="#1e1e1e").pack(anchor="w")
        self.output = ScrolledText(right, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4",
                                   state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True, padx=5, pady=5)

        pane.add(left, width=600)
        pane.add(right)

    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def open_file(self):
        file = filedialog.askopenfilename()
        if file:
            with open(file, "r") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".l")
        if file:
            with open(file, "w") as f:
                f.write(self.editor.get("1.0", tk.END))

    def show_output(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")
        self.output.see(tk.END)

    def on_run(self):
        self.run_button.config(state="disabled")
        code = self.editor.get("1.0", tk.END)
        input_data = self.input_box.get("1.0", tk.END).strip()
        self.show_output("🛠 Compiling and Running...\n")

        def run_in_background():
            stdout, stderr = self.runner(code, stdin_input=input_data)
            print("▶ stdout:", repr(stdout))
            print("▶ stderr:", repr(stderr))

            result_output = ""
            if stdout.strip():
                # Remove prompt line if it contains user input
                lines = stdout.splitlines()
                if input_data and len(lines) > 1 and input_data in lines[0]:
                    result_output += "✅ Output:\n" + "\n".join(lines[1:]) + "\n"
                else:
                    result_output += "✅ Output:\n" + stdout
            if stderr.strip():
                result_output += "❌ Error:\n" + stderr
                result_output += "\n💡 Suggestion:\n" + self.suggestor(stderr)

            def finish():
                if result_output.strip():
                    final_output = result_output.strip()
                else:
                    final_output = (
                        "⚠️ Program ran but produced no output.\n\n"
                        f"🧪 Raw stdout: {repr(stdout)}\n"
                        f"🧪 Raw stderr: {repr(stderr)}"
                    )
                self.show_output(final_output)
                self.run_button.config(state="normal")

            self.root.after(0, finish)

        threading.Thread(target=run_in_background, daemon=True).start()
