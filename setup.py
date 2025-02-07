"""
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
DON'T DIRECTLY EXECUTE THIS FILE!
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
YOU SHOULD USE `build` FOR PACKAGING
"""

from setuptools import setup, find_packages

version      = "1.0.1"
author       = "emofalling"
author_email = "emofalling@dingtalk.com"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
packages = find_packages()
print(f"[INFO] packages: {packages}")
setup(name="mpyfileopt",
      version=version,        
      description="Efficient MicroPython Device File System Management Tool",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT",
      author=author,
      author_email=author_email,
      url="https://github.com/emofalling/MpyFileOpt-Python",

      install_requires=[
        "pyserial>=3.0"
      ],	
      entry_points={
        'console_scripts': [
            'mpyfopt=mpyfopt.mpyfopt:main',
        ],
      },
      python_requires='>=3.10',
      packages=packages,

      keywords=["mpyfileopt", "mpyfopt", "python", "micropython", "windows", "linux", "mac", "ampy"],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
      ]
     )

# def setup(
#     *,
#     name: str = ...,
#     version: str = ...,
#     description: str = ...,
#     long_description: str = ...,
#     long_description_content_type: str = ...,
#     author: str = ...,
#     author_email: str = ...,
#     maintainer: str = ...,
#     maintainer_email: str = ...,
#     url: str = ...,
#     download_url: str = ...,
#     packages: list[str] = ...,
#     py_modules: list[str] = ...,
#     scripts: list[str] = ...,
#     ext_modules: Sequence[Extension] = ...,
#     classifiers: list[str] = ...,
#     distclass: type[Distribution] = ...,
#     script_name: str = ...,
#     script_args: list[str] = ...,
#     options: Mapping[str, Incomplete] = ...,
#     license: str = ...,
#     keywords: list[str] | str = ...,
#     platforms: list[str] | str = ...,
#     cmdclass: Mapping[str, type[_Command]] = ...,
#     data_files: list[tuple[str, list[str]]] = ...,
#     package_dir: Mapping[str, str] = ...,
#     obsoletes: list[str] = ...,
#     provides: list[str] = ...,
#     requires: list[str] = ...,
#     command_packages: list[str] = ...,
#     command_options: Mapping[str, Mapping[str, tuple[Incomplete, Incomplete]]] = ...,
#     package_data: Mapping[str, list[str]] = ...,
#     include_package_data: bool = ...,
#     # libraries for `Distribution` or `build_clib`, not `Extension`, `build_ext` or `CCompiler`
#     libraries: list[tuple[str, _BuildInfo]] = ...,
#     headers: list[str] = ...,
#     ext_package: str = ...,
#     include_dirs: list[str] = ...,
#     password: str = ...,
#     fullname: str = ...,
#     # Custom Distributions could accept more params
#     **attrs: Any,
# ) -> Distribution: ...
#