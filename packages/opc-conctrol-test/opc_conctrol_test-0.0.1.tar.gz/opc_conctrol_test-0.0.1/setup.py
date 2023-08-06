import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="opc_conctrol_test",
  version="0.0.1",
  author="waylon",
  author_email="981889207@qq.com",
  description="opc控制",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)