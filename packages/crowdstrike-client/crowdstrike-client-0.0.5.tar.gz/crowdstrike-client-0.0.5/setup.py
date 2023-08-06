import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crowdstrike-client",
    version="0.0.5",
    author="Pyperanger",
    description="A Non-oficial crowdstrike client API",
    url="https://github.com/pyperanger/crowdstrike-client",
    project_urls={
        "Bug Tracker": "https://github.com/pyperanger/crowdstrike-client/issues",
    },
    packages=["crowdstrikeclient"],
    install_requires=[
        "requests"
    ],
    python_requires=">=3.6",
)
