# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from multiprocessing import Process, Queue, Lock
from importlib import import_module
from . pjjobs_config import PJJobsConfig
from . pjjobs_socket import JsonSocket


class PJJobsServer(JsonSocket):
    def __init__(self, xml_config):
        self.config = PJJobsConfig(xml_config)
        super(PJJobsServer, self).__init__(
                address=self.config.Server.Name,
                port=int(self.config.Server.Port))
        self.socket.bind(
            (self.config.Server.Name, int(self.config.Server.Port)))

    @staticmethod
    def run_job(conn_socket, job, lock, q_finish):
        job_class = PJJobsServer._get_job_class(job.job_class)
        if not job_class:
            raise ValueError(
                "Class could not be loaded for {0} Job".format(job.name))
            return # TODO ERROR 

        #TODO verify that is a PJJob instance
        
        job_class.run(job.data, lock)

        conn_socket.send_obj({'response': {'id': 0}})
        conn_socket.close()
        q_finish.put(job.id)

    @staticmethod
    def _get_job_class(module_class):
        job_class = None
        module = module_class

        i = module.rindex('.')
        module_name = module[:i]
        class_name = module[i + 1:]
        try:
            job_module = import_module(module_name)
            job_class = getattr(job_module, class_name)
        except Exception as e:
            raise ValueError(e)
            return

        if job_class:
            return job_class()

    def listen(self):
        self.socket.listen(int(self.config.Server.MaxConnections))

        job_id = 1
        q_finish = Queue()
        procs = {}
        locks = {}
        while True:
            (clt_socket, address) = self.socket.accept()
            clientsocket = JsonSocket(use_socket=clt_socket)

            job = self._get_jobs(clientsocket, job_id)
            job_id += 1

            if not job:
                clientsocket.close()
                continue

            lck = None
            if job.is_queued:
                if job.name not in locks:
                    locks[job.name] = Lock()
                lck = locks[job.name]

            p = Process(
                target=self.run_job,
                args=(clientsocket, job, lck, q_finish))
            procs[job.id] = p
            p.start()

            while True:
                # Ensure process join
                try:
                    tmp = q_finish.get(block=False)
                    pr = procs[tmp]
                    pr.join()                    
                    del procs[tmp]
                except:
                    break

    def _get_response_data(self, id_, message):
        return {
            'response': {
                'id': id_,
                'message': message
            }
        }

    def _get_jobs(self, conn_socket, id_):
        data = conn_socket.read_obj()
        job = None
        try:
            if 'job' not in data:
                conn_socket.send_obj(self._get_response_data(
                    1, 'Invalid data format. No job found.'))
                return
            if 'data' not in data:
                conn_socket.send_obj(self._get_response_data(
                    1, 'Invalid data format. No data found.'))
                return

            job_name = data['job']
            if job_name not in self.config.jobs:
                conn_socket.send_obj(self._get_response_data(
                    2, "Job {0} not defined.".format(job_name)))
                return

            t_def = self.config.jobs[job_name]
            job = JobInfo(
                job_name, id_, data['data'],
                bool(t_def.Queued), t_def.Class)

        except Exception as e:
            conn_socket.send_obj(self._get_response_data(
                99, "Undetermined error. {0}".format(e)))
            return

        return job


class JobInfo(object):
    def __init__(self, name, id_, data, is_queued, job_class):
        self.name = name
        self.id = id_
        self.data = data
        self.is_queued = is_queued
        self.job_class = job_class
        

class PJJobsClient(JsonSocket):
    def __init__(self, address, port):
        super(PJJobsClient, self).__init__(address, port)

    def connect(self):
        self.socket.connect((self._address, self._port))


class PJJob(object):
    def __init__(self):
        pass

    def _run(self, data):
        raise NotImplementedError(
            "_run() must be implemente by Job class.")

    def run(self, data, lock):
        if lock:
            lock.acquire()
        self._run(data)
        if lock:
            lock.release()
