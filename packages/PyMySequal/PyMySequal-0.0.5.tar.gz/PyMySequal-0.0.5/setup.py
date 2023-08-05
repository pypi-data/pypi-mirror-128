from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='PyMySequal',
  version='0.0.5',
  description='A Smiple MsSql API',
  long_description_content_type="text/markdown",
  url='',  
  author='Murali Tharan S',
  author_email='muralififa@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['SQL','MsSql','SQL using python','Pyodbc','SQL Connection'], 
  packages=find_packages(),
  install_requires=[''] 
)
