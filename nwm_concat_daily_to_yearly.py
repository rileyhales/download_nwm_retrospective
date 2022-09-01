# requires: nco
# conda install -c conda-forge nco pandas
# python >=3.10

# concat the daily netcdfs to yearly using NCO

import glob
import os
import subprocess
import sys

import netCDF4 as nc
import numpy as np

if __name__ == "__main__":
    year = int(sys.argv[1])
    wildcard = os.path.join(".", f"{year}_slim", f"*.nc")
    subprocess.call(f'ncecat {wildcard} -o nwm_retro_{year}_daily_streamflow.nc -u time -v streamflow', shell=True)
    ds = nc.Dataset(f'nwm_retro_{year}_daily_streamflow.nc', 'a')
    t_var = ds.createVariable('time', 'i4', ('time',))
    t_var.units = f'days since {year}-01-01 00:00:00'
    t_var.origin = f'{year}-01-01 00:00:00'
    t_var.time_unit = 'days'
    t_var.time_unit_short = 'D'
    t_var[:] = np.array(range(len(glob.glob(wildcard))))
    ds.sync()
    ds.close()
    subprocess.call(f'rm {wildcard}', shell=True)
