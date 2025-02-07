from setuptools import setup, find_packages
import mpyfopt
import serial

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
"""
def setup(
    *,
    name: str = ...,
    version: str = ...,
    description: str = ...,
    long_description: str = ...,
    long_description_content_type: str = ...,
    author: str = ...,
    author_email: str = ...,
    maintainer: str = ...,
    maintainer_email: str = ...,
    url: str = ...,
    download_url: str = ...,
    packages: list[str] = ...,
    py_modules: list[str] = ...,
    scripts: list[str] = ...,
    ext_modules: Sequence[Extension] = ...,
    classifiers: list[str] = ...,
    distclass: type[Distribution] = ...,
    script_name: str = ...,
    script_args: list[str] = ...,
    options: Mapping[str, Incomplete] = ...,
    license: str = ...,
    keywords: list[str] | str = ...,
    platforms: list[str] | str = ...,
    cmdclass: Mapping[str, type[_Command]] = ...,
    data_files: list[tuple[str, list[str]]] = ...,
    package_dir: Mapping[str, str] = ...,
    obsoletes: list[str] = ...,
    provides: list[str] = ...,
    requires: list[str] = ...,
    command_packages: list[str] = ...,
    command_options: Mapping[str, Mapping[str, tuple[Incomplete, Incomplete]]] = ...,
    package_data: Mapping[str, list[str]] = ...,
    include_package_data: bool = ...,
    # libraries for `Distribution` or `build_clib`, not `Extension`, `build_ext` or `CCompiler`
    libraries: list[tuple[str, _BuildInfo]] = ...,
    headers: list[str] = ...,
    ext_package: str = ...,
    include_dirs: list[str] = ...,
    password: str = ...,
    fullname: str = ...,
    # Custom Distributions could accept more params
    **attrs: Any,
) -> Distribution: ...
"""
setup(name="mpyfileopt",    
      version=mpyfopt.__version__,        
      description="Efficient MicroPython Device File System Management Tool",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="emofalling",
      author_email="emofalling@dingtalk.com",
      url="https://github.com/emofalling/MpyFileOpt-Python",
      install_requires=[
        "pyserial>=3.0"
      ],	
      license="MIT",
      entry_points={
        'console_scripts': [
            'mpyfopt=mpyfopt.mpyfopt:main',
        ],
      },
      python_requires='>=3.10',
      packages=find_packages()
     )
