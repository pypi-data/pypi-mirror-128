import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yggdrasil-address-cofob",
    version="0.0.1",
    author="cofob",
    author_email="c@cofob.ru",
    description="Small tool for converting yggdrasil addresses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.cofob.ru/cofob/yggdrasil-address",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires=["bitarray"],
)
