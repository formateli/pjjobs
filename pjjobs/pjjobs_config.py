# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import os
from xml.dom import minidom
from xml.parsers import expat

_SECTIONS=['Server', 'Logging', 'Jobs', 'Job', 'Redirect']


class _Section(object):
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.value = None

    def add_section(self, section):
        self.children.append(section)
        section.parent = self
        if section.value:
            setattr(self, section.name, section.value)
        else:
            setattr(self, section.name, section)

    def add_value(self, value):
        self.value = value


class PJJobsConfig(object):
    def __init__(self, xml_config):
        self._sections = _Section('pjjobs')
        self.jobs = {}
        try:
            dom = minidom.parse(xml_config)
            node = dom.getElementsByTagName('pjjobs')
            if not node:
                IOError("Invalid pjjobs configuration file.")
            self._get_data(self._sections, node[0])
            self._set_attributes()
            self._finish()
        except Exception as e:
            raise Exception(e)

    def _get_data(self, parent_section, node):
        for n in node.childNodes:
            if n.nodeName in ('#text', '#comment'):
                continue 

            section = _Section(n.nodeName)
            if n.nodeName in _SECTIONS:
                self._get_data(section, n)
            else:
                section.value = _get_xml_tag_value(n)
            parent_section.add_section(section)

    def _set_attributes(self):
        for section in self._sections.children:
            setattr(self, section.name, section)

    def _finish(self):
        for job in self.Jobs.children:
            for n in job.children:
                if n.name == 'Name':
                    self.jobs[n.value] = job
                    if not hasattr(job, 'Queue'):
                        setattr(job, 'Queued', 'False')


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
