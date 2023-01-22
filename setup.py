import setuptools

from discord.ext import utils

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

packages = ["discord.ext.utils"]

setuptools.setup(
    name="discord-ext-utils",
    author="cibere",
    author_email="cibere.dev@gmail.com",
    url="https://github.com/cibere/discord-ext-utils",
    project_urls={
        "Code": "https://github.com/cibere/discord-ext-utils",
        "Issue tracker": "https://github.com/cibere/discord-ext-utils/issues",
        "Discord/Support Server": "https://discord.gg/2MRrJvP42N",
    },
    version=utils.__version__,
    python_requires=">=3.10",
    install_requires=REQUIREMENTS,
    packages=packages,
    description=utils.__description__,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
)
