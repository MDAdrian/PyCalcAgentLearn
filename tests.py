# tests.py
# Adjust the import path below to where your get_files_info() is defined.
# Example structure: utils/file_tools.py  -> from utils.file_tools import get_files_info


from functions.get_files_info import get_files_info


def print_result(title: str, result: str, indent_for_error: int = 4):
    print(title)
    if result.startswith("Error:"):
        # Indent errors by 4 spaces, exactly like in your example
        print(" " * indent_for_error + result)
    else:
        # Each line is printed with a single leading space so it shows as " - ..."
        for line in result.splitlines():
            print(" " + line)


def main():
    # 1) current directory
    res1 = get_files_info("calculator", ".")
    print_result('get_files_info("calculator", "."):\nResult for current directory:', res1)

    print()  # blank line between blocks

    # 2) 'pkg' directory
    res2 = get_files_info("calculator", "pkg")
    print_result("get_files_info(\"calculator\", \"pkg\"):\nResult for 'pkg' directory:", res2)

    print()

    # 3) absolute path '/bin' (should error as outside working dir)
    res3 = get_files_info("calculator", "/bin")
    print_result('get_files_info("calculator", "/bin"):\nResult for \'/bin\' directory:', res3)

    print()

    # 4) parent directory '../' (should error as outside working dir)
    res4 = get_files_info("calculator", "../")
    print_result('get_files_info("calculator", "../"):\nResult for \'../\' directory:', res4)


if __name__ == "__main__":
    main()
