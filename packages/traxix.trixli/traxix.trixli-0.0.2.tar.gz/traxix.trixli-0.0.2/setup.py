from setuptools import setup, find_namespace_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

    setup(
        name="traxix.trixli",
        version="0.0.2",
        url="https://gitlab.com/traxix/trixli",
        packages=find_namespace_packages(),
        install_requires=required,
        scripts=["traxix/again", "traxix/f", "traxix/fr"],
        author="trax Omar Givernaud",
    )
