from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='eyad',
  version='0.0.1',
  description='very code for eyad',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='eyad',
  author_email='hashemshaiban@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='eyad',
  packages=find_packages(),
  install_requires=[''] 
)
