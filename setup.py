import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="file_unittest",
    version="0.0.3",
    author="Amentum",
    author_email="team@amentum.space",
    description="A file-based unit test framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amentumspace/file_unittest.git",
    packages=setuptools.find_packages(),
    install_requires=[],
)