from setuptools import setup, find_packages


setup(
    name='testing-random',
    version='0.6',
    license='MIT',
    author="Vishal Pandey",
    author_email='vishalpandeyviptsk@gmail.com',
    packages=find_packages('questions'),
    package_dir={'': 'questions'},
    # url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'django-rest-framework',
          'xlwt'
      ],

)