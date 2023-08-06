import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='CGPCLI',  
     version='1.1.8',
     author="Lesnikov Nikita, Victor Gradzyavichus",
     author_email="gvv@communigate.ru",
     description="Package for CGP CLI access",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.6'
 )