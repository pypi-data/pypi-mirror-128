from setuptools import setup, find_packages

setup_args = dict(
    name = 'justanunsuspectingmodule',
    version = '1.1',
    description='Class with a module for lab',
    license='MIT',
    packages=find_packages(),
    author = 'Mekatto', 
    author_email = 'igor@mekatto.com',
    url = 'https://github.com/Igor-Sviridov/justanunsuspectingmodule',
    download_url = 'https://pypi.org/project/justanunsuspectingmodule/',
    python_requires='>3.6.0',
)

install_requires = [
          'scikit-commpy',
          'numpy',
          'soundfile',
          'bitstring',
          'scikit-learn',
          'matplotlib',
          'requests',

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
