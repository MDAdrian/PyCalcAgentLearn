# tests.py
# Adjust the import path to match where your get_file_content function lives.
import subprocess
from functions.get_files_info import get_files_info, get_file_content
from functions.run_file import format_completed_process, run_python_file
from functions.write_files import write_file

def print_result(title: str, result: str):
    print(title)
    print("-" * len(title))

    if result.startswith("Error:"):
        print("    " + result)
        return

    # If truncated, print only preview + marker
    if "[...File" in result:
        print("Preview (first 300 chars):")
        print(result[:300] + "...\n")
        print("✅ Truncation marker detected at the end:")
        print(result[-120:])  # Show last part with marker
    else:
        # File fits entirely — print it all
        print("Full file content:\n")
        print(result)

def print_result_write(title: str, result: str):
    print(title)
    print("-" * len(title))
    if result.startswith("Error:"):
        print("    " + result)
    else:
        print(result)
    print()  # blank line between tests

def print_case(title: str, result: str) -> None:
    print(title)
    print("-" * len(title))
    print(result if result else "No output produced.")
    print()  # blank line between cases


def main():
    # res = get_file_content("calculator", "lorem.txt")
    # print_result('get_file_content("calculator", "lorem.txt"):\nResult for lorem.txt:', res)

    # # 1) main.py inside calculator
    # res1 = get_file_content("calculator", "main.py")
    # print_result('get_file_content("calculator", "main.py"):\nResult for "main.py":', res1)
    # print()

    # # 2) pkg/calculator.py
    # res2 = get_file_content("calculator", "pkg/calculator.py")
    # print_result('get_file_content("calculator", "pkg/calculator.py"):\nResult for "pkg/calculator.py":', res2)
    # print()

    # # 3) outside working directory — should return an error
    # res3 = get_file_content("calculator", "/bin/cat")
    # print_result('get_file_content("calculator", "/bin/cat"):\nResult for "/bin/cat":', res3)
    # print()

    # # 4) non-existent file — should return an error
    # res4 = get_file_content("calculator", "pkg/does_not_exist.py")
    # print_result('get_file_content("calculator", "pkg/does_not_exist.py"):\nResult for missing file:', res4)

    # # 1️⃣ Write to a file inside working directory
    # res1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print_result_write('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):', res1)

    # # 2️⃣ Write to a file inside a subdirectory
    # res2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print_result_write('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):', res2)

    # # 3️⃣ Attempt to write outside the working directory
    # res3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print_result_write('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):', res3)

        # 1) should print the calculator's usage instructions
    cp1 = run_python_file("calculator", "main.py")
    print_case('run_python_file("calculator", "main.py")', cp1)

    # 2) run the calculator with an expression (may render "nasty" output)
    cp2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print_case('run_python_file("calculator", "main.py", ["3 + 5"])', cp2)

    # 3) run the calculator's own tests.py
    cp3 = run_python_file("calculator", "tests.py")
    print_case('run_python_file("calculator", "tests.py")', cp3)

    # 4) outside working directory -> error
    cp4 = run_python_file("calculator", "../main.py")
    print_case('run_python_file("calculator", "../main.py")', cp4)

    # 5) nonexistent file -> error
    cp5 = run_python_file("calculator", "nonexistent.py")
    print_case('run_python_file("calculator", "nonexistent.py")', cp5)

    # 6) not a Python file -> error
    cp6 = run_python_file("calculator", "lorem.txt")
    print_case('run_python_file("calculator", "lorem.txt")', cp6)



if __name__ == "__main__":
    main()
