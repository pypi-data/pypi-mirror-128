#!/usr/bin/env python3
# encoding: utf-8

import os
#from distutils.core import setup, Extension
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils import sysconfig

class custom_build_ext(build_ext):
	def build_extensions(self):
		# Override the compiler executables. Importantly, this
		# removes the "default" compiler flags that would
		# otherwise get passed on to to the compiler, i.e.,
		# distutils.sysconfig.get_var("CFLAGS").
		#print(distutils.sysconfig._config_vars)
		compiler = sysconfig.get_config_vars("CC")
		self.compiler.set_executable("compiler_so", compiler)
		self.compiler.set_executable("compiler_cxx", compiler)
		self.compiler.set_executable("linker_so", compiler)
		build_ext.build_extensions(self)

#os.environ["CC"] = "gcc"
compile_args = ["-w", "-Dlv",  "-Dis_cube_pruning", "-Dis_candidate_list",  "-std=c++11"] # -Wall -O2"]
#compile_args = ["-Wno-sign-compare -std=c++11"] # -Wall -O2"]
link_args	= []
#deps = "src/LinearFoldEval.cpp src/LinearFold.h src/Utils/energy_parameter.h src/Utils/feature_weight.h src/Utils/intl11.h src/Utils/intl21.h src/Utils/intl22.h src/Utils/utility_v.h src/Utils/utility.h".split(' ') 

module = Extension('LinearFold',
			language='c++',
			extra_compile_args=compile_args,
			extra_link_args=link_args,
			include_dirs=[
						 '.',
						 '...',
						 os.path.join(os.getcwd(), 'src'),
						 os.path.join(os.getcwd(), 'src/Utils'),
			],
			library_dirs = [os.getcwd(),],
			sources = ['src/python.cpp'] ) #, 'src/LinearFold.cpp']  )

def readme():
	with open("README.md", "r") as fh:
		long_desc = fh.read()
	return long_desc

def get_version():
	with open("VERSION", 'r') as f:
		v = f.readline().strip()
		return v

def main():
	setup (
		name = 'LinearFold',
		version = get_version(),
		author = "Katelyn McNair, Liang Huang*, He Zhang**, Dezhong Deng**, Kai Zhao, Kaibo Liu, David Hendrix, David Mathews",
		author_email = "deprekate@gmail.com",
		description = 'A a tool to predict RNA secondary structure and minimum free energy',
		long_description = readme(),
		long_description_content_type="text/markdown",
		url =  "https://github.com/LinearFold/LinearFold",
		scripts=[],
		classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
			"Operating System :: OS Independent",
		],
		python_requires='>3.5.2',
		packages=find_packages(),
		#install_requires=[''],
		ext_modules = [module],
		#cmdclass={"build_ext":custom_build_ext}
		#cmdclass={"build_ext":build_ext}
	)


if __name__ == "__main__":
	main()
