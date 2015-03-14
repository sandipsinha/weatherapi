#!/bin/bash -e

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ ! -d "$BASEDIR/ve" ]; then
    virtualenv -q $BASEDIR/ve --no-site-packages
    echo "Virtualenv created."
fi
. $BASEDIR/ve/bin/activate
if [ ! -f "$BASEDIR/ve/updated" -o $BASEDIR/requirements.txt -nt $BASEDIR/ve/updated ]; then
    pip install -r $BASEDIR/requirements.txt 
    touch $BASEDIR/ve/updated
    echo "Requirements installed."
fi
. $BASEDIR/ve/bin/activate
python run.py

