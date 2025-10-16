# tests.py
# Adjust the import path to match where your get_file_content function lives.
from functions.get_files_info import get_files_info, get_file_content

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


def main():
    # res = get_file_content("calculator", "lorem.txt")
    # print_result('get_file_content("calculator", "lorem.txt"):\nResult for lorem.txt:', res)

    # 1) main.py inside calculator
    res1 = get_file_content("calculator", "main.py")
    print_result('get_file_content("calculator", "main.py"):\nResult for "main.py":', res1)
    print()

    # 2) pkg/calculator.py
    res2 = get_file_content("calculator", "pkg/calculator.py")
    print_result('get_file_content("calculator", "pkg/calculator.py"):\nResult for "pkg/calculator.py":', res2)
    print()

    # 3) outside working directory — should return an error
    res3 = get_file_content("calculator", "/bin/cat")
    print_result('get_file_content("calculator", "/bin/cat"):\nResult for "/bin/cat":', res3)
    print()

    # 4) non-existent file — should return an error
    res4 = get_file_content("calculator", "pkg/does_not_exist.py")
    print_result('get_file_content("calculator", "pkg/does_not_exist.py"):\nResult for missing file:', res4)


if __name__ == "__main__":
    main()
