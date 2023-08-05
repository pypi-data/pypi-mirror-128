import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="fastapi_cls",
  version="0.1.1",
  author="yfengli",
  author_email="lizhichao@lilith.com",
  description="FastAPI framework class view router",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Carlos-Zen/fastapi_cls",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)