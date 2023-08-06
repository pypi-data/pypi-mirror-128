import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
      name='mandaw',
      version='2.3.0',
      description='A 2D GameEngine Made In Python With PySDL2',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='mandaw2014',
      author_email='mandawbuisness@gmail.com',
      url='https://mandaw2014.github.io/MandawEngineSDL/',
      packages=['mandaw'],
      package_dir={'':'mandaw_engine'},
      python_requires=">=3.6",
      install_requires=["pysdl2", "pysdl2-dll"]
)