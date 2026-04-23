import os
import logging
from pathlib import Path
from urllib.parse import urlparse
from contextlib import contextmanager

logger = logging.getLogger(__name__)

def path_with_repo(base, url, branch=None):
    ''' build a file system path with git repo url and branch name '''
    if not branch:
        branch = ''
    logger.debug(f'parsing {url}')
    parsed = urlparse(url)
    return Path(
        base,
        parsed.netloc,
        parsed.path.lstrip('/'),
        branch
    )

