from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='persian_fluency_detector',
    version='1.0.0',
    description='This library calculates the fluency factors of a given audio file It is important that the file formats be wave You can customize the speech to text tool the default speech to text is VOSK',
    long_description=readme,
    author='Nbic',
    long_description_content_type="text/markdown",
    packages=find_packages(include=["persian_fluency_detector*"]),
    url="https://github.com/salsina/persian-fluency-detector",
    install_requires=[],

    keywords=['python', 'first package'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)