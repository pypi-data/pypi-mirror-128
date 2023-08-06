import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
f = open("requirements.txt","w")
f.write('requests'+'\n'+'json'+'\n'+'mechanize'+'\n'+'uuid'+'\n'+'secrets'+'\n'+'os'+'\n'+'random'+'\n'+'time'+'\n'+'telepot')

fr = open("requirements.txt",'r')
requires = fr.read().split('\n')
    
setuptools.setup(
    name="TrackCobra",
    version="0.2.0",
    author="Mr GPS",
    author_email="MrGps00@gmail.com",
    description="Short EveryThing In Seconds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrGps1",
    project_urls={
        "Bug Tracker": "https://github.com/MrGps1/MrGps/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
