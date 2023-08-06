from distutils.core import setup
from io import open

def read(f):
    return open(f, 'r', encoding='utf-8').read()

setup(
  name = 'ml-dl-models',         # How you named your package folder (MyLib)
  packages = ['ml_dl_models'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Module to access ml dl models.',   # Give a short description about your library
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  author = 'Laxman Maharjan',                   # Type in your name
  author_email = 'lxmnmrzn17@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/laxmanmaharjan/ml-dl-models',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/laxmanmaharjan/ml-dl-models/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['ml', 'dl','ml_dl_models', 'models'],   # Keywords that define your package best
  install_requires=[            # Write the Dependencies
          'pip>=21',
          'music21',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)

