#!/bin/bash

## bash
export FREESURFER_HOME=/Applications/freesurfer/
source $FREESURFER_HOME/SetUpFreeSurfer.sh

## tcsh
setenv FREESURFER_HOME /Applications/freesurfer/
source $FREESURFER_HOME/SetUpFreeSurfer.csh

$1