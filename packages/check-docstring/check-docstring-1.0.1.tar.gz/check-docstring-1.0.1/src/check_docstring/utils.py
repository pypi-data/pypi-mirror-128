"""
Format checker for Python docstrings.

Date: 2021/11/19
"""


import re


def check_func_docstring_section(text, indent, section, func_args=None):
    """
    Check a particular section in a function docstring.

    Args:
        text (str): Section text.
        indent (int): Indentation in number of spaces for this function docstring.
        section (str): Section name => Args, Returns, Raises.
        func_args (list): List of function input argument names.

    Returns:
        True if all good; False otherwise.
    """

    success = True

    if text:

        if text[-1] != "\n":
            success = False

        # Process each line
        for line in text[:-1].split("\n"):

            # Compute the indentation for this line
            _indent = len(line) - len(line.lstrip())

            # The 1st indentation level under a section
            if _indent == indent + 4:

                # For Args, check its pattern and see if every input argument is
                # documented
                if section == "Args":
                    match = re.search(
                        r"^ +((?P<arg_name>\w+) \([^\(\)]+?\): .+|None|N/A)\.?$", line
                    )
                    if not match:
                        success = False
                        break

                    arg_name = match.group("arg_name")
                    if arg_name in func_args:
                        func_args.remove(arg_name)

                # For Raises, check its pattern
                elif section == "Raises":
                    if not re.search(r"^ +\w+: .+$", line):
                        success = False
                        break

            # The 2nd indentation level under a section
            elif _indent == indent + 8:
                pass

            # Unknown indentation level
            else:
                success = False
                break

    if not success:
        print(f"Wrong '{section}' format!")

    elif func_args:
        print(f"Missing args: {', '.join(func_args)}")
        success = False

    return success


def check_func_docstring_txt(func_args, docstring):
    """
    Check a particular function docstring.

    Args:
        func_args (list): List of function input argument names.
        docstring (str): Function docstring text.

    Returns:
        True if all good; False otherwise.
    """

    lines = docstring.split("\n")

    # There has to be at least 7 lines
    if len(lines) < 7:
        print("There should be at least 7 lines in function docstring!")
        return False

    # Different from common convention, our agreed docstring pattern is empty on the
    # 1st and last lines
    if lines[0] or lines[-1].strip():
        print("First and last line should be empty!")
        return False

    # If the 2nd line is empty, the description section is empty
    if not lines[1]:
        print("No description!")
        return False

    # Check indentation
    for line in lines[1:]:
        line_lstrip = line.lstrip()
        _indent = len(line) - len(line_lstrip)
        if _indent % 4 != 0:
            print("Wrong indentation!")
            return False

    # Check general docstring pattern
    indent = len(lines[1]) - len(lines[1].lstrip())
    match = re.search(
        rf"\S+\n\n {{{indent}}}Args:\n(?P<args>[\s\S]*?)\n {{{indent}}}Returns:\n(?P<returns>[\s\S]*?)(\n {{{indent}}}Raises:\n(?P<raises>[\s\S]*?))? {{{indent}}}$",
        docstring,
    )
    if not match:
        print("Wrong docstring pattern!")
        return False

    # Check 'Args' section
    if not check_func_docstring_section(match.group("args"), indent, "Args", func_args):
        return False

    # Check 'Returns' section
    if not check_func_docstring_section(match.group("returns"), indent, "Returns"):
        return False

    # Check 'Raises' section
    if not check_func_docstring_section(match.group("raises"), indent, "Raises"):
        return False

    return True


def check_func_docstrings(text):
    """
    Check all function docstrings in the input script text.

    Args:
        text (str): Input script text.

    Returns:
        True if all good; False otherwise.
    """

    success = True

    # Parse the script text to find every function docstring
    for result in re.finditer(
        r" *def \w+\((?P<func_args>[^\(\)]*)\):\n +\"{3}(?P<func_docstring>[\s\S]*?)\"{3}",
        text,
    ):
        # Get the function input arguments and docstring
        func_args = result.group("func_args").split(",")
        func_args = [x.strip().split("=")[0] for x in func_args if x.strip()]
        func_docstring = result.group("func_docstring")
        for arg in ["cls", "self", "*args", "**kwargs"]:
            if arg in func_args:
                func_args.remove(arg)

        # Check this docstring; print its line number and content if it's a bad one
        if not check_func_docstring_txt(func_args, result.group("func_docstring")):
            line_number = text[: result.start("func_docstring")].count("\n")
            print(f"Line {line_number}:")
            print("> " + "\n> ".join(func_docstring.split("\n")))
            print()
            success = False

    return success


def check_module_docstrings():
    """
    Check module docstring format. Currently not implemented.

    Args:

    Returns:
    """


def check_class_docstrings():
    """
    Check class docstring format. Currently not implemented.

    Args:

    Returns:
    """
