import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mysql-toolbox",
    version="0.0.13",
    description="MySQL toolbox.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/walkerever/mysql-toolbox",
    author="Yonghang Wang",
    author_email="wyhang@gmail.com",
    license="Apache 2",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ "xtable","xmltodict"],
    keywords=[ "mysql","toolbox"],
    entry_points={ "console_scripts": 
        [ 
            "mysql-replication-display=toolbox:repl_main", 
            "mysql-xml-formatter=toolbox:xml_formatter_main", 
        ] 
    },
)
