import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='discself',  
     version='1.0.0',
     author="elijahgives",
     description="A simple discord selfbot client.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=["discself"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )