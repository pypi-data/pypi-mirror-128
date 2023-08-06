from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ArukovicSonicMathility',
  version='0.0.1',
  description='Math module to make your life easier!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Arukovic',
  author_email='preston20201976@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Math', 
  packages=find_packages(),
  install_requires=[''],
)