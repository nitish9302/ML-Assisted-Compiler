from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai
import os

# ✅ Set your OpenAI API key securely (from env var or secret manager)
openai.api_key = os.getenv("sk-svcacct-teaPs3-lGUdL3IoMUYHMRu2PnWG5X5NSKYKgUEK9DLF2UnGT3BlbkFJOYKZpyVD0Zfdv4qkJMgtwo9qOohZICsu6EhGOE2W55pLdqwA")

# ✅ Use a compact model for local matching
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Sample extended dataset of error messages
KNOWN_ISSUES = [
    {"error": "undefined reference to `main", "fix": "Make sure you have a 'main' function defined in your Lex or C code."},
    {"error": "yywrap", "fix": "Add 'int yywrap() { return 1; }' to your Lex file."},
    {"error": "implicit declaration of function", "fix": "Ensure all used functions are declared or included properly with headers like <stdio.h>."},
    {"error": "expected identifier or '('", "fix": "Check your syntax. You may have missed a semicolon or used a reserved keyword."},
    {"error": "command not found", "fix": "Make sure Flex, GCC, and other dependencies are installed and added to PATH."},
    {"error": "unrecognized rule", "fix": "Check your Lex rules. Correct format: 'pattern  { action }'."},
    {"error": "multiple definition of", "fix": "You're likely defining a function or variable more than once. Check for duplicates."},
    {"error": "no rule to make target", "fix": "Check filenames and paths. Ensure Makefile targets and file names are correct."},
    {"error": "lex.yy.c: No such file or directory", "fix": "Flex didn't generate 'lex.yy.c'. Verify syntax in your .l file."},
    {"error": "redefinition of", "fix": "Avoid defining the same variable or function multiple times."},
    {"error": "incompatible type for argument", "fix": "Make sure function arguments match expected types."},
    {"error": "undeclared (first use in this function)", "fix": "Declare variables before using them. Did you miss a header or declaration?"},
    {"error": "expected ';'", "fix": "You probably missed a semicolon at the end of a statement."},
    {"error": "ISO C forbids", "fix": "You're likely using a deprecated syntax. Consider modern C practices."},
    {"error": "unused variable", "fix": "Remove or use the declared variable to avoid warnings or errors."},
    {"error": "segmentation fault", "fix": "You're accessing invalid memory. Check pointer usage and array bounds."},
    {"error": "invalid suffix", "fix": "You may have mistyped a literal or used incorrect suffix (e.g. '10LZ')."},
    {"error": "syntax error before", "fix": "Check for missing braces, semicolons, or data types."},
    {"error": "expected expression before", "fix": "Verify that you've declared the symbol or used correct syntax before the expression."},
    {"error": "conflicting types for", "fix": "Ensure function declarations match their definitions."},
    {"error": "too few arguments to function", "fix": "You're passing fewer arguments than required by the function."},
    {"error": "too many arguments to function", "fix": "You're passing more arguments than the function accepts."},
    {"error": "'struct' has no member named", "fix": "Check if the struct member exists and is correctly spelled."},
    {"error": "error: stray '\\", "fix": "You've likely included a non-ASCII or invisible character. Remove or retype the line."},
    {"error": "cannot find -l", "fix": "A required library is missing. Install it or link it correctly in your compiler flags."},
    {"error": "multiple definition of 'main'", "fix": "You may have multiple files with 'main'. Only one is allowed."},
    {"error": "invalid preprocessing directive", "fix": "Check your #define/#include syntax. Remove invalid directives."},
    {"error": "expected '=', ',', ';', 'asm' or '__attribute__'", "fix": "You likely forgot to assign or terminate a declaration."},
    {"error": "incomplete type is not allowed", "fix": "You're using a type that hasn't been fully defined yet."}
]

# ✅ Prepare local embedding database
error_texts = [e["error"] for e in KNOWN_ISSUES]
fix_texts = [e["fix"] for e in KNOWN_ISSUES]
embeddings = model.encode(error_texts)

def suggest_fix(error_msg):
    """
    Uses vector similarity to suggest fix. Falls back to GPT if unknown.
    """
    if not error_msg:
        return "No error message to analyze."

    query_embedding = model.encode([error_msg])[0]
    scores = cosine_similarity([query_embedding], embeddings)[0]
    best_idx = np.argmax(scores)

    if scores[best_idx] > 0.5:
        return fix_texts[best_idx]
    else:
        return gpt_fallback(error_msg)

def gpt_fallback(error_msg):
    """
    Uses OpenAI's GPT to generate a helpful fix when local match fails.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a programming assistant that fixes C and Lex compiler errors."},
                {"role": "user", "content": f"The user encountered this error:\n\n{error_msg}\n\nHow can they fix it?"}
            ],
            temperature=0.2,
            max_tokens=150
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ GPT fallback failed: {e}"

