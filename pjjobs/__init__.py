# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import sys
import os
import logging
from . pjjobs import PJJobsServer, PJJobsClient, PJJob
from . logger import PJJobsLog

PROJECT_NAME = 'PJJobs'
AUTHOR = 'Fredy Ramirez'
COPYRIGHT = '2018, Fredy Ramirez - http://www.formateli.com'
LICENSE = 'GNU GENERAL PUBLIC LICENSE V3'
VERSION = '0.1.0'
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

#LOGGER = PJJobsLog(get_config_value('logging', 'logger_level', 'DEBUG'))
LOGGER = None

