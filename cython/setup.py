import os

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# os.environ["CFLAGS"] = "-I{}".format(CURRENT_DIR)
os.environ["LDFLAGS"] = "-L{}".format(CURRENT_DIR)

ext_modules=[
    Extension("spam", ["spam.pyx"], libraries=["my"]) # Unix-like specific
]

setup(
  name = "Spam",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)