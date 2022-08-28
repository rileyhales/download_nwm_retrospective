# requires: pandas, nco
# conda install -c conda-forge nco pandas
# python >=3.10

# convert the hourly netcdfs to daily using NCO

import os
import datetime
import subprocess
import pandas as pd
import sys


if __name__ == "__main__":
    year = int(sys.argv[1])

    daterange = pd.date_range(
        datetime.date(year, 1, 1),
        datetime.date(year, 12, 31),
        freq="D"
    )
    for date in daterange:
        wildcard_path = os.path.join(".", f"{year}_slim", f"{date.strftime('%Y%m%d')}*")
        subprocess.call(f'nces {wildcard_path} -o {year}_slim_daily/{date.strftime("%Y%m%d")}.nc --op_typ mean', shell=True)
        subprocess.call(f'rm {wildcard_path}', shell=True)
