import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sebyga",
    version="0.0.4",
    author="Seongbin Ga",
    author_email="sebyga@gmail.com",
    keywords = ['adsorption','PSA','process simulation','breakthrough curve'],
    description="Python package for adsorption simulations",
    long_descrption= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebyga/pyAPEP",
    packages=setuptools.find_packages(),
    license="PNU_Seongbin_Ga",
    python_requires= ">=3.5",
    install_requires = ['numpy','scipy']
)

print(long_description)

