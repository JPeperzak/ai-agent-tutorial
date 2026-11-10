import os

def list_files():
    return os.listdir(".")

# The "with" keyword simplifies resource management by automatically handling setup and cleanup through context managers.
# This means that we do not need to explicitly close the opened file, but that this is automatically handled through the with keyword
def read_file(filename):
    with open(filename, "r") as file:
        return file.read()

def count_lines(filename):
    with open(filename, "r") as file:
        return len(file.readlines())