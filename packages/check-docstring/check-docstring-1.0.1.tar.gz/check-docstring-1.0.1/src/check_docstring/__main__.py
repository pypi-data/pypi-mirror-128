import os
import sys
from .utils import check_func_docstrings


# Collect python scripts from the input argument
input_path = sys.argv[1]
input_files = []

if os.path.isdir(input_path):
    for path, _, files in os.walk(input_path):
        for file in files:
            input_files.append(os.path.join(path, file))
elif os.path.isfile(input_path):
    input_files = [input_path]
input_files = [f for f in input_files if f.lower().endswith(".py")]

# Exit if no scripts collected
if not input_files:
    print("No Python scripts collected!")
    sys.exit()

success = True

# Check docstrings
print()
print("Checking function docstrings...")
for file in input_files:
    print(file)
    with open(file, "r", encoding="utf-8") as file:
        text = file.read()
        if not check_func_docstrings(text):
            success = False

# Die on failure
if success:
    print("All good!")

print()
