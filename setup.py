from setuptools import setup
import os

def remove(path):
  """
  Remove a file or a directory recursively using terminal commands.
  This way avoid some permissions errors.
  """
  if os.path.exists(path):
    if os.name == "nt": os.system(("rd /s" if os.path.isdir(path) else "del /f") + " /q \"" + path.replace('/', '\\') + "\"")
    else: os.system("rm -rf \"" + path.replace('\\', '/') + "\"")

def clean_pycache(path="."):
  """Clean __pycache__ directories before running setup()."""
  for file in os.listdir(path):
    new_path = os.path.join(path, file)
    if os.path.isdir(new_path): 
      if file == "__pycache__": remove(new_path)
      else: clean_pycache(new_path)


with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

clean_pycache(__file__[:__file__.rfind("\\")+1 or __file__.rfind("/")+1])
setup(
  name="ion-numworks",
  version="2.0",
  author="ZetaMap",
  description="The porting of 'Ion module, from Numworks, for PC.",
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
  packages=[
    "ion",
    "ion.util",
    "ion.util.stuff"
  ],
  package_data={"": ["**"]},
  install_requires=["pynput"],
  python_requires= '>=3.6',
)
