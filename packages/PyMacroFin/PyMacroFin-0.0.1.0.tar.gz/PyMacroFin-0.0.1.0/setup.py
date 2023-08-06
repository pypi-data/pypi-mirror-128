import setuptools

with open("README.txt","r") as f:
    mylong_description = f.read()

setuptools.setup(   name='PyMacroFin',
                    version='0.0.1.0',
                    #py_modules=['./finance_byu/__init__','./finance_byu/regtables'],
                    packages=['PyMacroFin'],
                    package_data={'':['*.txt']},
                    classifiers=["Programming Language :: Python :: 3",
                                 "Operating System :: OS Independent",
                                 "License :: OSI Approved :: MIT License"],
                    description="Python toolbox for solving continuous-time macro-financial models using monotone finite difference schemes",
                    long_description=mylong_description,
                    project_urls={"Documentation":"https://adriendavernas.com/pymacrofin/index.html"},
                    long_description_content_type="text/markdown",
                    install_requires = ['numpy',
                                        'pandas',
                                        'joblib',
                                        'scipy',
                                        'plotly>=5.0.0',
                                        'sympy',
                                        'dash>=2.0.0',
                                        'flask',
                                        'cloudpickle',
                                        'dash_daq',
                                        'kaleido',
                                        'findiff'],
                    license='MIT',
                    python_requires='>=3.6',
                    author="Damon Petersen",
                    author_email="damon.petersen@chicagobooth.edu"
                )