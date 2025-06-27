import subprocess
import os
import platform
from .utils import ensure_temp_dir, get_temp_path

def run_lex_code(code, yacc_code=None, stdin_input=None):
    ensure_temp_dir()

    lex_file = get_temp_path("user_code.l")
    with open(lex_file, "w") as f:
        f.write(code)

    output_binary = get_temp_path("output.exe" if is_windows() else "output")

    try:
        print("➡ Running flex...")
        flex_result = subprocess.run(["flex", lex_file], capture_output=True, text=True)
        print("✔ flex output:", flex_result.stdout)
        if flex_result.returncode != 0:
            print("❌ flex error:", flex_result.stderr)
            return "", f"Lex failed:\n{flex_result.stderr}"

        print("➡ Compiling with gcc...")
        gcc_result = subprocess.run(["gcc", "lex.yy.c", "-o", output_binary], capture_output=True, text=True)
        print("✔ gcc output:", gcc_result.stdout)
        if gcc_result.returncode != 0:
            print("❌ gcc error:", gcc_result.stderr)
            return "", f"GCC failed:\n{gcc_result.stderr}"

        print("➡ Executing binary...")
        run_result = subprocess.run(
            [output_binary],
            input=stdin_input or "",
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✔ Program output:", run_result.stdout)
        return run_result.stdout, run_result.stderr

    except subprocess.TimeoutExpired:
        return "", "⏱ Program timed out. It may be waiting for input."
    except Exception as e:
        return "", f"⚠️ Unexpected error:\n{str(e)}"

def is_windows():
    return platform.system().lower().startswith("win")
