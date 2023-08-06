from setuptools import setup

f = open("README.md", "r")
README = f.read()

setup(
    name="multipurpose-discord",
    author="MrPotato",
    url="",
    version='0.0.1',
    packages=['multipurposediscord'],
    license='MIT',
    description="A package made for multipurpose stuff!",
    long_description_content_type="text/markdown",
    long_description=README,
    install_requires=[],
    python_requires='>=3.5.3',
    include_package_data=True,
    keywords=[
        'discord.py', 
        'discord', 
        'discord-multipurpose'
    ]
)