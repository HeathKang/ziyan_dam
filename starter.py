
from __future__ import absolute_import

__author__ = "mabo.io"
__copyright__ = "mabo.io"
__license__ = "MIT"
__version__ = "0.2.4"

import os
import sys
# find the plugins
sys.path.append(os.getcwd())


from ziyan.main import main


if __name__ == '__main__':
    
    appname = "ziyan"
    
    main(appname)