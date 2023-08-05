import os
from distutils import sysconfig
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

name_package = 'text2ipa'
fnames = ['text2ipa']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ext_modules = [ 
    Extension(
        "text2ipa",
        [f"./src/{name_package}/{file}.cpp" for file in fnames],
        include_dirs=['.'],
        language='c++',
    ),
]

class BuildExt(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        ext = os.path.splitext(filename)[1]
        return filename.replace(suffix, f"/{name_package}{ext}")

    def build_extensions(self):
        build_ext.build_extensions(self)

setup(
    ext_modules=ext_modules,
	cmdclass={'build_ext': BuildExt},
)
