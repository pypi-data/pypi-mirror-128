from setuptools import setup

setup(
  name='fmdl',
  version='0.0.6',
  description = "Failure Mode Definition Language Compiler",
  author = "Michael A. Hicks",
  author_email = "michael@mahicks.org",
  url = "https://mahicks.org",
  scripts=['fmc'],
  packages=['pytransform'],
  py_modules=['fmc','csv2fmdlrequirements'],
  package_data={'pytransform':['platforms/darwin/x86_64/_pytransform.dylib','platforms/windows/x86/_pytransform.dll','platforms/windows/x86_64/_pytransform.dll','platforms/linux/x86/_pytransform.so','platforms/linux/x86_64/_pytransform.so']},
  license = "Proprietary",
  python_requires=">3.8,<3.10"
)
