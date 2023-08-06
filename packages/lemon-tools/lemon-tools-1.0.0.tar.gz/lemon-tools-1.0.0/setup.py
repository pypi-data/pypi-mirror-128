import pathlib
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="lemon-tools",
      version="1.0.0",
      # if you want a cleaner versioning use the things below
      # setup_requires=['setuptools_scm'],
      # intall_requires=['setuptools_scm'],
      # use_scm_version={'write_to': 'lemon-tools/version.txt'},
      description="Module buider with CI included",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/japandotorg/lemon-tools",
      author="Lemon Rose", author_email="yash.kul69@gmail.com",
      packages=find_packages(),
      test_suite='tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      scripts=['scripts/lemon-make-package'],
      zip_safe=False
      )