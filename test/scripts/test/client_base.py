#!/usr/bin/env python

# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import os
import sys

try:
    input = raw_input # Python2-3
except NameError:
    pass

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

try:
    from pjjobs import PJJobsClient    
except ImportError:
    print('Running uninstalled mode...')
    DIR = os.path.normpath(
        os.path.join(DIRECTORY, '..', '..', '..', 'pjjobs'))
    if os.path.isdir(DIR):
        sys.path.insert(0, os.path.dirname(DIR))
    from pjjobs import PJJobsClient


SERVER = 'localhost'
PORT = 9009


class ClientTest(object):
    def __init__(self, job_name):
        self.job_name = job_name
    
    def run(self):
        bucle = input('Bucle: ')
        
        data = {
            'job': self.job_name,
            'data': {
                'bucle': int(bucle)
            }
        }
        
        clientsocket = PJJobsClient(SERVER, PORT)
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


if __name__ == "__main__":	

    bucle = input('Bucle: ')
    
    data = {
        'job': 'TestBucle',
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
