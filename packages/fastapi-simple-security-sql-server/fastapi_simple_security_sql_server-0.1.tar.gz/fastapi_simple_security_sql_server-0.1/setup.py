from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fastapi_simple_security_sql_server',
    version='0.1',    
    description="API key based security package for FastAPI, focused on simplicity of use",
    url="https://github.com/karmalegend/fastapi_simple_security",
    author='Bart Ouwerkerk',
    author_email='b.ouwerkerk@mvgm.nl',
    license="MIT",
    packages=["fastapi_simple_security"],
    install_requires=["fastapi","pyodbc"],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)