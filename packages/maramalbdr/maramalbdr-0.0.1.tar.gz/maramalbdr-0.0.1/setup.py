from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='maramalbdr',
  version='0.0.1',
  description='simple code for maramalbdr',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='hashemshaiban',
  author_email='hashemshaiban@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='maramalbdr',
  packages=find_packages(),
  install_requires=[''] 
)
