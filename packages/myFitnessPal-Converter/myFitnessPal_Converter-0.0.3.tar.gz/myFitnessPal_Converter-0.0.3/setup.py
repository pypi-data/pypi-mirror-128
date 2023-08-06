from setuptools import setup, find_packages

classifiers = [
  'Programming Language :: Python :: 3',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent'
]


setup(
  name='myFitnessPal_Converter',
  version='0.0.3',
  author='Youssef Sultan',
  author_email='youssefsultann@gmail.com',
  description='For converting myFitnessPal CSV exports to monthly or daily exports',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  license='MIT',
  classifiers=classifiers,
  keywords='MyFitnessPal',
  packages=find_packages(),
  install_requires=['pandas'],
  url ='https://github.com/youssefsultan/myFitnessPal_Converter'
)
