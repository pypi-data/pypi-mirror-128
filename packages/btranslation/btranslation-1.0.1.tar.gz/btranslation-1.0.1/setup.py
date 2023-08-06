from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Back Translator using Google translation API'

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        'License :: OSI Approved :: MIT License',
        "Operating System :: Microsoft :: Windows",
    ]

# Setting up
setup(
    name="btranslation",
    version=VERSION,
    author="Sumit Mishra",
    author_email="<sumit.mishra0432@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['googletrans', 'pandas', 'numpy'],
    keywords=['python', 'NLP', 'back transaltion', 'text augmentation', 'google translation API'],
    
)
