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
    name = "Pigeon Data Processor",
    version = "0.1",
    description = "Program used to process experimental data from studies run on pigeons involving a comparison on peck location with relation to a goal target in geometry and feature driven learning environments.",
    author = "Chris Cadonic",
    options = {"build_exe": build_exe_options},
    executables = [Executable("dataProcessor.py")]
)
