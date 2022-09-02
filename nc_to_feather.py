import glob
import os

import netCDF4 as nc
import pandas as pd
from natsort import natsorted

for f in natsorted(glob.glob("nwm_retro_*_daily_streamflow.nc")):
    ds = nc.Dataset(f)
    year = int(os.path.basename(f).replace('nwm_retro_', '').replace('_daily_streamflow.nc', ''))
    df = pd.DataFrame(
        ds['streamflow'][:],
        columns=ds['feature_id'][:].flatten().astype(str),
        index=pd.to_datetime(ds['time'][:].flatten(), unit='D', origin=ds['time'].origin)
    ).rename_axis('datetime').reset_index().to_feather(f'nwm_retro_{year}_daily_streamflow.feather')
    ds.close()
