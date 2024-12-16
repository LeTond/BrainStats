#!/bin/bash

cd /Applications/freesurfer/subjects

## bash
export FREESURFER_HOME=/Applications/freesurfer/subjects
source $FREESURFER_HOME/SetUpFreeSurfer.sh

recon-all $1 -i $2 -s $3 $4


