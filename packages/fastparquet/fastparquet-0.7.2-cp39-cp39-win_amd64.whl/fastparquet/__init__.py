"""parquet - read parquet files."""


""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_9():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'fastparquet.libs'))
    if sys.version_info[:2] >= (3, 8):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load_order')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_9()
del _delvewheel_init_patch_0_0_9
# end delvewheel patch


__version__ = "0.7.2"

from .thrift_structures import parquet_thrift
from .core import read_thrift
from .writer import write
from . import core, schema, converted_types, api
from .api import ParquetFile
from .util import ParquetException
