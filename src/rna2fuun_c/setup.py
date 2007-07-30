# setup.py
import distutils
from distutils.core import setup, Extension

setup(name = "rna2fuun C Implementation",
      version = "2.5",
      ext_modules = [Extension("rna2fuun_c", ["rna2fuun_c.i","rna2fuun.cpp"], swig_opts = ['-c++'])])
