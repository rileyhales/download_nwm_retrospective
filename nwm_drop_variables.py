import glob
import os
import subprocess
import sys

if __name__ == '__main__':
    year = int(sys.argv[1])
    for nc in glob.glob(os.path.join(f'{year}_daily', '*')):
        subprocess.call(f'ncks -v streamflow {nc} {year}_slim/{os.path.basename(nc)}', shell=True)
        subprocess.call(f'rm {nc}', shell=True)
