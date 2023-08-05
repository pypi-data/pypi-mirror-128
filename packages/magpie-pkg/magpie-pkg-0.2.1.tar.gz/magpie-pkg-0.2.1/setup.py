import setuptools
from numpy.distutils.core import setup, Extension

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

#ext1 = Extension(name='magpie.src.utils', sources=['magpie/src/utils.f90'])
ext1 = Extension(name='magpie.src.remap_utils', sources=['magpie/src/remap_utils.f90'])
ext2 = Extension(name='magpie.src.remap_1d_grid2grid', sources=['magpie/src/remap_1d_grid2grid.f90'])
ext3 = Extension(name='magpie.src.remap_2d_grid2grid', sources=['magpie/src/remap_2d_grid2grid.f90'])
ext4 = Extension(name='magpie.src.remap_3d_grid2grid', sources=['magpie/src/remap_3d_grid2grid.f90'])

exts = [ext1, ext2, ext3, ext4]#, ext5]

setup(name = 'magpie-pkg',
      version = '0.2.1',
      description       = "Monte cArlo weiGhted PIxel rEmapping",
      long_description  = long_description,
      long_description_content_type = 'text/markdown',
      url               = 'https://github.com/knaidoo29/magpie',
      author            = "Krishna Naidoo",
      author_email      = "krishna.naidoo.11@ucl.ac.uk",
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['numpy', 'matplotlib', 'healpy'],
      ext_modules = exts,
      python_requires = '>=3',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Mathematics',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      )
