#!/usr/bin/env sh
# generated from catkin/cmake/template/setup.sh.in

# Sets various environment variables and sources additional environment hooks.
# It tries it's best to undo changes from a previously sourced setup file before.
# Supported command line options:
# --extend: skips the undoing of changes from a previously sourced setup file

SETUP_UTIL="/home/julian/aaad/interactive-manipulation-sandbox/binfrastructure/ros/src/executer_actions/build/devel/_setup_util.py"

if [ ! -f "$SETUP_UTIL" ]; then
  echo "Missing Python script: $SETUP_UTIL"
  return 22
fi

# detect if running on Darwin platform
UNAME=`which uname`
UNAME=`$UNAME`
IS_DARWIN=0
if [ "$UNAME" = "Darwin" ]; then
  IS_DARWIN=1
fi

# make sure to export all environment variables
export CMAKE_PREFIX_PATH
export CPATH
if [ $IS_DARWIN -eq 0 ]; then
  export LD_LIBRARY_PATH
else
  export DYLD_LIBRARY_PATH
fi
export PATH
export PKG_CONFIG_PATH
export PYTHONPATH

# invoke Python script to generate necessary exports of environment variables
MKTEMP=`which mktemp`
SETUP_TMP=`$MKTEMP /tmp/setup.sh.XXXXXXXXXX`
$SETUP_UTIL $@ > $SETUP_TMP
. $SETUP_TMP
rm $SETUP_TMP

# remember type of shell if not already set
if [ -z "$CATKIN_SHELL" ]; then
  CATKIN_SHELL=sh
fi

# run all environment hooks
FIND=`which find`
SORT=`which sort`
ENV_HOOKS_GENERIC=$($FIND "/home/julian/aaad/interactive-manipulation-sandbox/binfrastructure/ros/src/executer_actions/build/devel/etc/catkin/profile.d" -maxdepth 1 -name "*.sh" 2>/dev/null | $SORT)
if [ "$CATKIN_SHELL" != "sh" ]; then
  ENV_HOOKS_SPECIFIC=$($FIND "/home/julian/aaad/interactive-manipulation-sandbox/binfrastructure/ros/src/executer_actions/build/devel/etc/catkin/profile.d" -maxdepth 1 -name "*.$CATKIN_SHELL" 2>/dev/null | $SORT)
else
  ENV_HOOKS_SPECIFIC=
fi
for envfile in $ENV_HOOKS_GENERIC $ENV_HOOKS_SPECIFIC; do
  . "$envfile"
done
