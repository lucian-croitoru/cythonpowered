#!/bin/bash
# run with "source dev_venv.sh" to rebuild and enter the virtualenv
# run "chmod u+x dev_venv.sh" if getting "Permission denied" on above command
# run "source venv/bin/activate" just to activate the virtualenv without rebuilding
# run "deactivate" to exit
# run "sudo apt-get install python3-pip python3-dev python3-venv" if packages not installed

rm -rf $PWD/.venv			    # delete .venv
python3 -m venv $PWD/.venv		# create .venv
source $PWD/.venv/bin/activate	# activate .venv

# set environment variables for first use
export PYTHONPATH=$PWD:$PYTHONPATH
export PYTHONPATH=$PWD/tests:$PYTHONPATH
export PYTHONPATH=$PWD/benchmark:$PYTHONPATH

# append PYTHONPATH to the "activate" script - for persistent use
echo -e "export PYTHONPATH="$PYTHONPATH >> $PWD/.venv/bin/activate

# install requirements
pip3 install -r requirements.txt

# build
python3 setup.py build
