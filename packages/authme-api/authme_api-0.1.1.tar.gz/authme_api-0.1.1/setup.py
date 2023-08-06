import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="authme_api",
    version="0.1.1",
    description="MySQL API for AuthMe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.cofob.ru/cofob/authme_api",
    install_requires=["mysql-connector-python"],
    package_dir={"": "src"},
    packages=["authme_api"],
    python_requires=">=3.6",
)
