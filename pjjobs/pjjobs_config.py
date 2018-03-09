# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import os
from xml.dom import minidom
from xml.parsers import expat


class PJJobsConfig(object):
    def __init__(self, xml_config):
        self.server_name = None
        self.server_port = None
        self.server_max_connections = None
        self.jobs = {}

        try:
            dom = minidom.parse(xml_config)
            node = dom.getElementsByTagName('pjjobs')
            self._get_data(node[0])
        except Exception as e:
            raise Exception(e)

    def _get_data(self, node):
        for n in node.childNodes:
            if n.nodeName in ('#text', '#comment'):
                continue
            if n.nodeName == 'Server':
                self._get_server(n)
            if n.nodeName == 'Jobs':
                self._get_jobs(n)

    def _get_server(self, node):    
        for n in node.childNodes:
            if n.nodeName in ('#text', '#comment'):
                continue
            if n.nodeName == 'Name':
                self.server_name = _get_xml_tag_value(n)
            if n.nodeName == 'Port':
                self.server_port = int(_get_xml_tag_value(n))
            if n.nodeName == 'MaxConnections':
                self.server_max_connections = int(_get_xml_tag_value(n))

    def _get_jobs(self, node):
        for n in node.childNodes:
            if n.nodeName in ('#text', '#comment'):
                continue
            if n.nodeName != 'Job':
                continue
            job = Job(n)
            self.jobs[job.name] = job


class Job(object):
    def __init__(self, node):
        self.name = None
        self.queued = False
        self.job_class = None
    
        for n in node.childNodes:
            if n.nodeName in ('#text', '#comment'):
                continue
            if n.nodeName == 'Name':
                self.name = _get_xml_tag_value(n)
            if n.nodeName == 'Queued':
                q = _get_xml_tag_value(n)
                self.queued = bool(q)
            if n.nodeName == 'Class':
                self.job_class = _get_xml_tag_value(n)


def _get_xml_tag_value(node):
    'Returns the valid value of xml node'
    xml_str = node.toxml()
    start = xml_str.find('>')
    if start == -1:
        return
    end = xml_str.rfind('<')
    if end < start:
        return
    res = _unescape(xml_str[start + 1:end])
    return res


def _unescape(s):
    # want_unicode = False
    if not isinstance(s, str):
        s = s.encode("utf-8")
    # if isinstance(s, unicode):
    #     s = s.encode("utf-8")
    #     want_unicode = True

    # the rest of this assumes that `s` is UTF-8
    list = []

    # create and initialize a parser object
    p = expat.ParserCreate("utf-8")
    p.buffer_text = True
    # p.returns_unicode = want_unicode
    p.CharacterDataHandler = list.append

    # parse the data wrapped in a dummy element
    # (needed so the "document" is well-formed)
    p.Parse("<e>", 0)
    p.Parse(s, 0)
    p.Parse("</e>", 1)

    # join the extracted strings and return
    es = ""
    # if want_unicode:
    #     es = u""
    return es.join(list)
