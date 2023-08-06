import click
import os


PYPROJECT_TOML = """
[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
"""

SETUP_CFG = """
[metadata]
name = {}
version = 0.0.1
author = {}
author_email = author@example.com
description = A small example package
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/pypa/sampleproject
project_urls =
    Bug Tracker = https://github.com/pypa/sampleproject/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.6

[options.packages.find]
where = src

"""

READ_ME_FILE_CONTENT  = """
Hello {} is the best python project :)

"""

LICENSE_CONTENT  = """
Copyright (c) 2021 {}
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


def create_file_in_src(name: str, file: str, content: str | None = None) -> bool:
    try:
        if content == None:
            with open(f"{name}/src/{file}", mode="w"):
                return True
        elif type(content) == str and content != None:
            with open(f"{name}/src/{file}", mode="w") as f:
                f.write(content)
    except:
        return False

def create_file_in_example_project(name: str, file: str, content: str | None = None) -> bool:
    try:
        if content == None:
            with open(f"{name}/src/example_project/{file}", mode="w"):
                return True
        elif type(content) == str and content != None:
            with open(f"{name}/src/example_project/{file}", mode="w") as f:
                f.write(content)
    except:
        return False

@click.command()
@click.option('--name', help="Name of the project")
@click.option('--author', help="Author/Publisher of the project")
def create_project(name, author):
    if os.path.exists(name):
            click.echo(click.style(f"{name} already exists", fg="red"))
            return
    else: 
        if click.confirm(f"Hey Pythoneer or Pythonista, are you sure you want to name your project {name}"):
            click.echo(f"Started creating a Pypi project {name}")
            os.mkdir(name)
            os.mkdir(f"{name}/src")
            os.mkdir(f'{name}/src/example_project')
            click.secho(f"Made a directory named {name}", fg="green")

            create_file_in_src(name, "pyproject.toml", PYPROJECT_TOML)
            click.secho("Created project.toml", fg="green")

            create_file_in_src(name, "setup.cfg", content=SETUP_CFG.format(name, author))
            click.secho("Created setup.cfg", fg="green")

            create_file_in_src(name, "README.md", content=READ_ME_FILE_CONTENT.format(name))
            click.secho("Created README.md", fg="green")
            create_file_in_src(name, "LICENSE", content=LICENSE_CONTENT.format(author))
            click.secho("Created LICENSE file with defualt license", fg="green")
            click.secho("You can a different license from https://choosealicense.com/", fg="blue")
            create_file_in_example_project(name, "__init__.py", content=None)
            create_file_in_example_project(name, "main.py", "print('Hello World')")
            click.secho(f"Sucessfully created Pypi project: {name}", fg="yellow")
        else:
            click.echo(click.style("Done Cancelling the Program", fg="red"))
