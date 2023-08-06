"""Commond Line Interface"""

from sys import argv

from sqlfmt.core import fix


def main():
    """Main function for CLI."""
    file_path = argv[1]

    with open(file_path, "r") as f:
        origin_query = f.read()

    fixed_query = fix(origin_query)

    with open(file_path, "w") as f:
        f.write(fixed_query)


if __name__ == "__main__":
    main()
