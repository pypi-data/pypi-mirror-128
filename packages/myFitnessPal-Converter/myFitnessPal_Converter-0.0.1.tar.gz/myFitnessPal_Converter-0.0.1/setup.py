from setuptools import setup, find_packages

classifiers = [
  'Programming Language :: Python :: 3',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent'
]


setup(
  name='myFitnessPal_Converter',
  version='0.0.1',
  author='Youssef Sultan',
  author_email='youssefsultann@gmail.com',
  description='For converting myFitnessPal CSV exports to monthly or daily exports',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  license='MIT',
  classifiers=classifiers,
  keywords='MyFitnessPal',
  packages=find_packages(),
  install_requires=['pandas'],
  url ='https://github.com/youssefsultan/myFitnessPal_Converter'
)
