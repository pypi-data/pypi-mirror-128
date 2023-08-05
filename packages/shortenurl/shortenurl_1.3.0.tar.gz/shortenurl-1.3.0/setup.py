from setuptools import find_packages, setup

with open("README.md", encoding="UTF-8") as f:
    long_desc = f.read()

setup(
    name='shortenurl',
    description='Shorten URLs with Python',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    version='1.3.0',
    url='https://github.com/s4300/shortenurl-python',
    author='s4300',
    author_email='',
    license='NONE',
    keywords='shorten urls tinyurl bitly url',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
)