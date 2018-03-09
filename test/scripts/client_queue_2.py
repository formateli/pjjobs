#!/usr/bin/env python

# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import os
import sys

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

try:
    from pjjobs import PJJobsClient
    
except ImportError:
    print('Running uninstalled mode...')
    DIR = os.path.normpath(os.path.join(DIRECTORY, '..', '..', 'pjjobs'))
    if os.path.isdir(DIR):
        sys.path.insert(0, os.path.dirname(DIR))
    from pjjobs import PJJobsClient


if __name__ == "__main__":	

    bucle = raw_input('Bucle: ')
    
    data = {
        'job': 'TestBucleQueue2',
        'data': {
            'bucle': int(bucle)
        }
    }
    
    clientsocket = PJJobsClient('LOCALHOST', 9009)
    clientsocket.connect()
    clientsocket.send_obj(data)
    
    while True:
        data = clientsocket.read_obj()
        if data['response']['id'] == 0:
            print("OK RECEIVED !")
            break
        else:
            print(data['response']['message'])
            break
    clientsocket.close()

