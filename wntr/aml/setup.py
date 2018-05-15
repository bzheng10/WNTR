from setuptools import setup, find_packages
from setuptools.extension import Extension
import shutil
import numpy
import os

try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

print('********************************')
print(numpy_include)
print('********************************')

ipopt_executable = shutil.which('ipopt')

if ipopt_executable is None:
    raise RuntimeError('Ipopt not in path. Installation unsuccessful')
else:
    print('Ipopt found in {}'.format(ipopt_executable))

ipopt_bin = os.path.dirname(ipopt_executable)
ipopt_base = os.path.dirname(ipopt_bin)
ipopt_include = os.path.join(ipopt_base, 'include', 'coin')
ipopt_include_third_party = os.path.join(ipopt_include, 'ThirdParty')
ipopt_lib = os.path.join(ipopt_base, 'lib')

# inplace extension module
project_dir = os.path.dirname(os.path.abspath(__file__))
src_files = os.path.join(project_dir, 'aml')
expression_i = os.path.join(src_files, 'expression.i')
expression_cxx = os.path.join(src_files, 'expression.cpp')
component_i = os.path.join(src_files, 'component.i')
component_cxx = os.path.join(src_files, 'component.cpp')
wntr_model_i = os.path.join(src_files, 'wntr_model.i')
wntr_model_cxx = os.path.join(src_files, 'wntr_model.cpp')
ipopt_model_i = os.path.join(src_files, 'ipopt_model.i')
ipopt_model_cxx = os.path.join(src_files, 'ipopt_model.cpp')
aml_tnlp_cxx = os.path.join(src_files, 'aml_tnlp.cpp')

extension_modules = list()

expression_ext = Extension("aml._expression",
                           sources=[expression_i, expression_cxx],
                           language="c++",
                           extra_compile_args=["-std=c++11"],
                           include_dirs=[numpy_include, src_files],
                           library_dirs=[],
                           libraries=[],
                           swig_opts=['-c++'])
extension_modules.append(expression_ext)

component_ext = Extension("aml._component",
                           sources=[component_i, component_cxx],
                           language="c++",
                           extra_compile_args=["-std=c++11"],
                           include_dirs=[numpy_include, src_files],
                           library_dirs=[],
                           libraries=[],
                           swig_opts=['-c++'])
extension_modules.append(component_ext)

wntr_model_ext = Extension("aml._wntr_model",
                           sources=[wntr_model_i, wntr_model_cxx],
                           language="c++",
                           extra_compile_args=["-std=c++11"],
                           include_dirs=[numpy_include, src_files],
                           library_dirs=[],
                           libraries=[],
                           swig_opts=['-c++'])
extension_modules.append(wntr_model_ext)

ipopt_model_ext = Extension("aml._ipopt_model",
                            sources=[ipopt_model_i, ipopt_model_cxx, aml_tnlp_cxx],
                            language="c++",
                            extra_compile_args=["-std=c++11"],  # , "-stdlib=libc++"],
                            include_dirs=[numpy_include, src_files, ipopt_include],
                            library_dirs=[ipopt_lib],
                            libraries=[os.path.join(ipopt_lib, 'ipopt')],
                            swig_opts=['-c++'])
extension_modules.append(ipopt_model_ext)

for i in extension_modules:
    print(i)

setup_kwargs = {
    'requires': [],
    'scripts': [],
}

setup(name="aml",
      description="Python AML and AD",
      author="Michael Bynumm",
      version="0.0",
      packages=['aml'],
      ext_modules=extension_modules,
      **setup_kwargs
    )
