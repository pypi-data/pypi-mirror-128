import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="anslapi",
  version="1.0.1",
  author="anttin",
  author_email="muut.py@antion.fi",
  description="Module for creating a simple API with AWS Lambda and API Gateway",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/anttin/anslapi",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ]
)
