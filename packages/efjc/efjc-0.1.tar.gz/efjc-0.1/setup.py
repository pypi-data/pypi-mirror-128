from distutils.core import setup
setup(
  name = 'efjc',         # How you named your package folder (MyLib)
  packages = ['efjc'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The extensible freely-joined chain (EFJC) single-chain model Python package.',   # Give a short description about your library
  author = 'Michael R. Buche',                   # Type in your name
  author_email = 'mrbuche@sandia.gov',      # Type in your E-Mail
  url = 'https://github.com/mbuche/efjc',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mbuche/efjc/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['efjc', 'polymer', 'single', 'chain', 'model', 'statistical', 'mechanics', 'thermodynamics'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 1 - Planning',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)

# See:
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56