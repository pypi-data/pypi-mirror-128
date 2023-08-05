# BD RD Docstring Checker

## Usage

```bash
check_docstring PATH
```

where `PATH` can be a file or a directory. All Python scripts will be collected and checked.

## Docstring Convention

Google style docstring [ref1](https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format/24385103#24385103) [ref2](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings) [ref3](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

```python
def example_function(param1, param2):
    """
    This is an example of a function docstring.
    More descriptions go here.

    Args:
        param1 (int): The first parameter.
            Second line has to be indented.
        param2 (str): The second parameter.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `param2` is equal to `param1`.
    """

    if param1 == param2:
        raise ValueError('param1 may not be equal to param2')
    return True
```

---
Last updated: 2021/11/19
