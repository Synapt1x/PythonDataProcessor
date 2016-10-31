# DataProcessor
____
###Created by: Chris Cadonic
###For: Dr. Debbie Kelly lab
----
## Building
### Pre-requisites
In order to build this program, the build system must have *Python 2.7* installed. With Python installed, you will also need the following packages:

+*numpy*
+*pandas*
+*Tkinter*
+*glob*
+*xlsWriter*
+*cx-Freeze*

If you need any of these packages installed, or aren't sure if they are updated/installed, you can simply run

```pip install (package name)```

in a terminal window.

The easiest way to install Python along with most of the above packages in one fell swoop is to install *Anaconda 2*. It is a Python distribution package that includes many of the most commonly required packages for Python applications. You can install it [from here](https://www.continuum.io/downloads "Anaconda download site"). 

If there are still remaining packages that need be installed after installing Anaconda, then you can do this by running the following in a terminal

```conda install (package name)```

This should only be true of *cx-Freeze*, however, which would require:

```conda install cx-Freeze```

if Anaconda is installed, or

```pip install cx-Freeze```

if you prefer to remain using pip.

### Building Process
Once the system is prepared to build, you can simply open a terminal window and then navigate to the directory in which the program was extracted to. Here you should find *dataProcessor.py*, *pigeon.py*, *ToolTip.py*, and *setup.py*. The setup Python file will call *cx-Freeze* to build the executeable. To do this, run the following command in the terminal window

```python setup.py build```

This will create a *build* directory alongside the program Python files. Inside this directory, there should be a sub-directory indicating the operating system and python version of the current build, which in this case was 64-bit Windows OS running Python 2.7. Thus the sub-directory will likely be *exe.win-amd64-2.7*. Inside here is where the executeable is located. It will be called **dataProcessor.exe**. Once built, you can simply run this executeable directly or from a link to this file.
