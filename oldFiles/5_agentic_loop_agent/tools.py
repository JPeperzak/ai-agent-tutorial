import os

def list_files():
    contents = [file for file in os.listdir('.') if os.path.isfile(os.path.join('.', file))]
    return contents

def count_lines(filename):
    with open(filename, "r") as file:
        return len(file.readlines())