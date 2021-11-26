#!/usr/bin/python3
import sys, os

# How many characters should be shown at least for each directory level?
min_chars_shown = 3
# Look for matches only for directories. This results in potentially shorter
# strings, but copying those partially might, if the last component is shortened,
# also match files and thus, might surprise you
glob_only_on_directories = False

# get $HOME to use ~
home = os.path.normpath(os.environ['HOME'])
# do this for all paths given by lines on stdin; if used inside a prompt,
# usually only one line (the current directory) is given
for path in sys.stdin:
    # normalize path and remove trailing newlines
    path = os.path.normpath(path.rsplit('\n')[0])
    # check if that path exists and is a directory
    if not os.path.isdir(path):
        print("(not dir)")
        sys.exit(1)
    # Check if that path is within $HOME. If so, replace $HOME with ~ and set
    # remaining search path accordingly; if not: start with absolute path
    # instead
    if path.startswith(home):
        buildpath = home
        remaining = path[len(home):]
        shortpath = '~'
    else:
        buildpath = os.sep
        remaining = path[1:]
        shortpath = os.sep
    # now go through each path component (directory)
    for component in remaining.split(os.sep):
        # find all subdirectories
        subdirs = [d for d in os.listdir(buildpath) if not glob_only_on_directories or os.path.isdir(os.path.join(buildpath, d))]
        # find the maximum length of a common prefix between the current component
        # and any subdirectory (to see where, if at all, to put the cut-off)
        # Set this to something larger than 0 to achieve a minimum length used
        maxcommon = min(min_chars_shown - 1, len(component))
        for subdir in subdirs:
            if subdir != component:
                common = os.path.commonprefix([subdir, component])
                maxcommon = max(maxcommon, len(common))
        # do not use "*" when it is not shorter to do so
        if (maxcommon >= len(component)-2):
            shortpath += component + os.sep
        # replace component name with shorter version
        else:
            shortpath += component[:maxcommon+1] + '*' + os.sep
        buildpath += component + os.sep
    print(shortpath)
