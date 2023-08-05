from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="check-docstring",
    description="BD RD docstring format checker.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="1.0.1",
    package_dir={"": "src"},
    include_package_data=True,
    scripts=["./scripts/check_docstring"],
    packages=find_packages(where="src"),
    python_requires=">=3.6.*",
    install_requires=[],
    extras_require={"dev": ["pytest>=5.4.3", "pytest-cov>=2.10.0"]},
)
