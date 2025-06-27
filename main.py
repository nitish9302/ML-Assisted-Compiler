import tkinter as tk
from frontend.gui import LexIDE
from core.runner import run_lex_code
from ml.suggestion_engine import suggest_fix

if __name__ == "__main__":
    root = tk.Tk()
    app = LexIDE(root, run_lex_code, suggest_fix)
    root.mainloop()
