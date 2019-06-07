import io
import os
import os.path as osp

from setuptools import find_packages, setup

import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

# Package meta-data.
NAME = 'mesh_intersection'
DESCRIPTION = 'PyTorch module for Mesh self intersection detection'
URL = ''
EMAIL = 'vassilis.choutas@tuebingen.mpg.de'
AUTHOR = 'Vassilis Choutas'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

here = os.path.abspath(os.path.dirname(__file__))

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError
# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

bvh_src_files = ['src/bvh.cpp', 'src/bvh_cuda_op.cu']
bvh_include_dirs = torch.utils.cpp_extension.include_paths() + [
    'include',
    osp.expandvars('$CUDA_SAMPLES_INC')]

bvh_extra_compile_args = {'nvcc': ['-DPRINT_TIMINGS=0', '-DDEBUG_PRINT=0',
                                   '-DERROR_CHECKING=0',
                                   '-DCOLLISION_ORDERING=1'],
                          'cxx': []}
bvh_extension = CUDAExtension('bvh_cuda', bvh_src_files,
                              include_dirs=bvh_include_dirs,
                              extra_compile_args=bvh_extra_compile_args)

render_reqs = ['pyrender>=0.1.23', 'trimesh>=2.37.6', 'shapely']

setup(name=NAME,
      version=about['__version__'],
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      python_requires=REQUIRES_PYTHON,
      url=URL,
      packages=find_packages(),
      ext_modules=[bvh_extension],
      install_requires=[
          'torch>=1.0.1.post2',
      ],
      extras_require={
          'render': render_reqs,
          'all': render_reqs
      },
      cmdclass={'build_ext': BuildExtension})