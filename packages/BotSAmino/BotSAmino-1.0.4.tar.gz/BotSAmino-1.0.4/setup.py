import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="BotSAmino",
    version="1.0.4",
    url="https://github.com/SirLez/BotSAmino",
    download_url="https://github.com/SirLez/BotSAmino/archive/refs/heads/main.zip",
    description="Amino Bots with python!",
    long_description=README,
    long_description_content_type="text/markdown",
    author="SirLez",
    author_email="SirLezDV@gmail.com",
    license="MIT",
    keywords=[
        "aminoapps",
        "amino-py",
        "amino",
        "amino-bot",
        "narvii",
        "api",
        "python",
        "python3",
        "python3.x",
        "ThePhoenix78",
        "AminoBot",
        "BotAmino",
        "botamino",
        "aminobot",
        "botaminew",
        "samino",
        "SAmino",
        "SirLez",
        "sirlez"
    ],
    include_package_data=True,
    install_requires=[
        "setuptools",
        "requests",
        "six",
        "websocket-client",
    ],
    setup_requires=["wheel"],
    packages=find_packages(),
)
