from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='monther',
  version='0.0.1',
  description='simple code for monther',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='monther',
  author_email='hashemshaiban@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='monther',
  packages=find_packages(),
  install_requires=[''] 
)
