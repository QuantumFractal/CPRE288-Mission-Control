# CPRE288-Mission-Control
The repository for our CPRE 288 project.


## Setup

#### Install system dependencies and virtual environment
This project requires python 2.7 and pip installed. Python 2.7 can be installed from [here](https://www.python.org/download/releases/2.7.8/). Pip is a package manager for python. [Follow the steps there to install Pip](https://pip.pypa.io/en/latest/installing.html)
(ensure that both can be run from the command line)

This project also requires the use of a Null-Modem emulator. This allows us to create a virtual Vortex and have it run on the same machine. [Download it for linux here](http://tty0tty.sourceforge.net/). [Download it for windows here](https://code.google.com/p/powersdr-iq/downloads/detail?name=setup_com0com_W7_x64_signed.exe&can=2&q=)

Once both are installed run the following commands to setup our virtual environment. A virtual environment is basically a folder with a python interpreter. It basically allows us to keep a clean python install separate from our systems install, reducing headaches from dependency conflicts.

Following the commands below to install virtualenv and setup one in your repo.
```Shell
$ pip install virtualenv
$ cd this_get_repo
$ virtualenv env
```
Now to "activate" your virtual environment, type
to get inside the environment
```Shell
$ source env/bin/activate
```

(Note: If on Windows run the following)
```Shell
$ ./env/scripts/activate.bat
```

Then run the following to download your dependencies for this project
```Shell
$ pip install -r requirements.txt
```
