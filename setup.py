from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ion-numworks",
    version="2.0",
    author="ZetaMap",
    description="The porting of the Ion module, from Numworks, for pc.",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ZetaMap/Ion-numworks",
    project_urls={
        "Bug Tracker": "https://github.com/ZetaMap/Ion-numworks/issues",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["keyboard"],
)
