from setuptools import setup

with open("README.md", "r") as fp:
    six_long_description = fp.read()

setup(
    name='cappuccino',
    version='0.1.4',
    packages=['Cappuccino'],
    url='https://github.com/vidigalp/cappuccino',
    license='',
    author='vidigalp',
    author_email='pedro.vidigal@instaclustr.com',
    description='Java GC Log Parser written in Python',
    long_description=six_long_description,
    long_description_content_type="text/markdown",
    install_requires = [
                           'numpy',
                           'pandas',
                           'python-dateutil',
                           'pytz',
                           'six',
                           'tqdm'
                       ],
)
