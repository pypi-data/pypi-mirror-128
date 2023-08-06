from distutils.core import setup


setup(
    name = 'sflcore',  # How you named your package folder (MyLib)
    packages = ['sflcore'],  # Chose the same as "name"
    version = '0.1',  # Start with a small number and increase it with every change you make
    license = 'MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'A system of useful classes and functions that will eventually form part of the BMPY standard library',
    # Give a short description about your library
    author = 'Max Curtis',  # Type in your name
    author_email = 'max.curtisenglandb@gmail.com',  # Type in your E-Mail
    url = 'https://github.com/Maaaax2021/sflcore',  # Provide either the link to your github or to your website
    download_url = 'https://github.com/Maaaax2021/sflcore/archive/refs/tags/V_0.1.tar.gz',  # I explain this later on
    keywords = ['BMPY', 'USEFUL', 'CORE'],  # Keywords that define your package best
    install_requires = [

        ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  #Specify which python versions that you want to support
        ],
    )
