#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

THISPATH=`dirname $0`

python $THISPATH/test_outputs.py