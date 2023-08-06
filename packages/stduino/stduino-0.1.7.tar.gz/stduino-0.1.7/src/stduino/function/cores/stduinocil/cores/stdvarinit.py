import os

from platform import system
platform_is=None
stdenv = None
projects_dir=None
if system() == "Windows" or system() == "cli":
    platform_is="Win"
    stdenv = os.environ["USERPROFILE"].replace('\\', '/')

    projects_dir = stdenv + "/Documents/Stduino/Projects/"
    username = os.environ['USERNAME']
elif system() == "Linux":
    platform_is="Linux"
    stdenv = os.environ["HOME"].replace('\\', '/')
    projects_dir = stdenv + "/Stduino/Projects/"
    username = os.environ['USERNAME']
    # ctags_path = stdinit.abs_path + "/tool/packages/ctagslin32/"
elif system() == "Darwin":
    platform_is = "Darwin"
    stdenv = os.environ["HOME"].replace('\\', '/')
    projects_dir = stdenv + "/Documents/Stduino/Projects/"
    username = os.environ['USER']
abs_path = os.path.abspath('.').replace('\\', '/')

try:
    if os.path.exists(projects_dir):
        pass
    else:
        os.makedirs(projects_dir)

except:
    pass
std_platform_dir=stdenv + "/.stduino/platforms"
try:
    if os.path.exists(std_platform_dir):
        pass
    else:
        os.makedirs(std_platform_dir)
except:
    pass
session_dir=stdenv + "/.stduino/session"
try:
    if os.path.exists(session_dir):
        pass
    else:
        os.makedirs(session_dir)

except:
    pass

#IDE
version_c = "0.0.1"#'1.01'

stdcache_dir=stdenv + "/.stduino/.cache"
try:
    if os.path.exists(stdcache_dir):
        pass
    else:
        os.makedirs(stdcache_dir)

except:
    pass
#signal

#sub ui

#project

project_name=None#new_workspace=stdinit.pro_dir_name
pro_dir_name=None#old_workfpace=stdinit.pro_dir_name

#debug&goto

