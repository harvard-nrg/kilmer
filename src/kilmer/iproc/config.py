import logging
import configparser

logger = logging.getLogger(__name__)

def parse(cfg):
    config = configparser.ConfigParser()
    config.read(cfg)
    return config

def get_outdir(cfg):
    config = parse(cfg)
    return config['iproc']['OUTDIR']
        
def get_resolution(cfg):
    config = parse(cfg)
    return config['out_atlas']['RESOLUTION']
