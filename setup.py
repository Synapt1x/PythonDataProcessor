from cx_Freeze import setup, Executable
build_exe_options = {
"includes": ['numpy', 'pandas'],
"packages": [],
'excludes' : ['boto.compat.sys',
              'boto.compat._sre',
              'boto.compat._json',
              'boto.compat._locale',
              'boto.compat._struct',
              'boto.compat.array',
              'collections.abc'],
"include_files": []}

setup(
    name = "simple",
    version = "0.1",
    description = "",
    author = "Dengar",
    options = {"build_exe": build_exe_options},
    executables = [Executable("simple.py")]
)
