import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ProjetoLPOL",
    version="0.0.1",
    author="Samuel Andrade",
    author_email="samueltech@live.com",
    description="Conversão de arquivos csv to json, json to csv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samueltechdev/ProjetoLPOL",
    project_urls={
        "Bug Tracker": "https://github.com/samueltechdev/ProjetoLPOL",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)