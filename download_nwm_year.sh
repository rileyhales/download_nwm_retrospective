#!/bin/bash

# requires aws cli
# current python environment needs dependencies of nwm_to_daily.py
# Download the national water model retrospective hourly data in netcdf format

echo "Year chosen is $1"

# download hourly
echo "Downloading hourly data"
mkdir "$1"
aws s3 cp s3://noaa-nwm-retrospective-2-1-pds/model_output/$1 ./$1 --no-sign-request --recursive --exclude "*" --include "19800101*CHRTOUT_DOMAIN1.comp" --include "19800102*CHRTOUT_DOMAIN1.comp"

# convert to daily
echo "Converting to daily"
mkdir "$1_daily"
python nwm_to_daily.py "$1"

# copy only streamflow variable to new files
echo "Dropping variables"
mkdir "$1_slim"
python nwm_drop_variables.py $1

# concatenate daily files to 1 yearly file
echo "Concatenating daily files"
python nwm_concat_daily_to_yearly.py $1

# zip for export
echo "Zipping"
zip -r "$1.zip" "nwm_retro_$1_daily_streamflow.nc"

# remove hourly and daily files
echo "Removing hourly and daily files"
rm -r "$1"
rm -r "$1_daily"
rm -r "$1_slim"
rm "nwm_retro_$1_daily_streamflow.nc"
