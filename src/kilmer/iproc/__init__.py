import logging
import pandas as pd

from .command import build_command
from . import config

logger = logging.getLogger(__name__)

def get_multiecho_scans(scanlist, tasklist):
    df1 = pd.read_csv(scanlist)
    df2 = pd.read_csv(tasklist)
    merged = pd.merge(df1, df2, on='TYPE', how='inner')
    result = merged.query('Analyze > 0 and NUMECHOS > 1')
    for _,scan in result.iterrows():
        yield scan
