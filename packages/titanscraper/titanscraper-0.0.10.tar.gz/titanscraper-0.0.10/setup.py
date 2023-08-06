from distutils.core import setup
setup(
    name = 'titanscraper',         # How you named your package folder (MyLib)
    packages = ['.'],   # Chose the same as "name"
    version = '0.0.10',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'A simple but yet powerfull scraping library',   # Give a short description about your library
    author = 'Emile DJIDA GONGDEBIYA',                   # Type in your name
    author_email = 'djidadevacc@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/emileKing/titanscraper',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/emileKing/titanscraper/archive/refs/tags/v.0.0.1.tar.gz',    # I explain this later on
    keywords = ['web scraping', 'web data collection' ],   # Keywords that define your package best
    install_requires=[      
        "beautifulsoup4==4.10.0",
        "bs4==0.0.1", 
        "lxml==4.6.3",
        "requests==2.26.0",
        "xmltodict==0.12.0"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license     
        'Programming Language :: Python :: 3.5', #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)