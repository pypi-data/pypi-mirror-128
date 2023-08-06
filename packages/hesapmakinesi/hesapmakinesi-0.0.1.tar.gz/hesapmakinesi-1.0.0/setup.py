from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='hesapmakinesi',
  version='1.0.0',
  description='hesaplama işlemlerinizi gerçekleştirmek için hazırladığım bir kütüphane',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/FADev01/hesap-makinesi',  
  author='Furkan Akbulut',
  author_email='akbulutfurkanDEV@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='hesap makinesi', 
  packages=find_packages(),
  install_requires=[''] 
)