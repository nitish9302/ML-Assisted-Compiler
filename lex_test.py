import subprocess

code = r'''
%{
#include <stdio.h>
%}
%%
[0-9]+    { printf("Number: %s\n", yytext); }
.|\n      { }
%%
int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
'''

# Step 1: Write user_code.l
with open("user_code.l", "w") as f:
    f.write(code)

try:
    # Step 2: Run flex
    flex = subprocess.run(["flex", "user_code.l"], capture_output=True, text=True)
    print("Flex Output:", flex.stdout)
    print("Flex Errors:", flex.stderr)
    if flex.returncode != 0:
        print("Flex failed")
        exit()

    # Step 3: Run gcc
    gcc = subprocess.run(["gcc", "lex.yy.c", "-o", "output.exe"], capture_output=True, text=True)
    print("GCC Output:", gcc.stdout)
    print("GCC Errors:", gcc.stderr)
    if gcc.returncode != 0:
        print("GCC failed")
        exit()

    # Step 4: Run the output.exe
    run = subprocess.run(["output.exe"], input="123\n", capture_output=True, text=True, timeout=5)
    print("Runtime Output:\n", run.stdout)

except Exception as e:
    print("Error:", str(e))
