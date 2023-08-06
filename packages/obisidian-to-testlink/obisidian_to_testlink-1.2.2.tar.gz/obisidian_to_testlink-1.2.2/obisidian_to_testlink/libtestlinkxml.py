# -*- coding: utf-8 -*-

import os
import sys
from xml.etree import ElementTree as ET

class BaseTestlinkxml():
    def __init__(self):
        pass

    def init_node(self, tag, attr = {}):
        node = ET.Element(tag, attrib = attr)
        return node

    def add_child_node(self, node, tag, attr = {}):
        child = ET.SubElement(node, tag, attrib = attr)
        return child

    def add_cdata(self, node, text):
        if isinstance(text, int):
            text = str(text)
        text = text.replace("\n", "<br />")
        node.append(ET.Comment(' --><![CDATA[' + text + ']]><!-- '))

    def show_node(self, node):
        pass

    def indent(self, elem, level=0):
        '''
        添加xml文件的换行符,增强可读性
        '''
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def write_xml(self, node, xml_path):
        w = ET.ElementTree(node)
        if not self.small:
            self.indent(node)
        w.write(xml_path, 'utf-8', True)

class LibTestlinkxml(BaseTestlinkxml):
    def __init__(self, small = False):
        self.small = small
        self.case_tag = {
                "ts":"testsuite",
                "tc":"testcase",
                "dt":"details",
                "sm":"summary",
                "cfs":"custom_fields",
                "cf":"custom_field",
                "sts":"steps",
                "st":"step",
                "sn":"step_number",
                "ac":"actions",
                "ep":"expectedresults",
                "pc":"preconditions",
                "ip":"importance",
                "et":"execution_type",
                "nm":"name",
                "val":"value",
                "kws":"keywords",
                "kw":"keyword",
            }
        self.req_tag = {
                "root":"requirement-specification",
                "rqs":"req_spec",
                "rq":"requirement",
                "id":"docid",
                "title":"title",
                "cfs":"custom_fields",
                "cf":"custom_field",
                "nm":"name",
                "val":"value",
                "dt":"scope",
                "sm":"description",
                "reqs":"requirements",
                "rst":"req_spec_title",
                "did":"doc_id",
                "rqt":"title"
                }
        self.req_id_dict = {}
        self.req_split = '#'

    def traverse_req(self, in_dict, node, root_id, req_type = '', reqs_path = '', id_count = 1):
        ts = self.add_child_node(node, self.req_tag['rqs'], attr = {
            "title":in_dict['title'],
            "doc_id":root_id
            })
        reqs_id = root_id
        reqs_path += self.req_split + in_dict['title']
        if "detail" in in_dict.keys() and in_dict['detail'] != '':
            dt = self.add_child_node(ts, self.req_tag['dt'])
        if "cases" in in_dict.keys() and in_dict['cases'] != []:
            for case in in_dict['cases']:
                req_id = reqs_id + "." +  str(id_count)
                id_count += 1
                tc = self.add_child_node(ts, self.req_tag['rq'])
                tt = self.add_child_node(tc, self.req_tag['title'])
                self.add_cdata(tt, case['title'])
                rid = self.add_child_node(tc, self.req_tag['id'])
                self.add_cdata(rid, req_id)
                self.req_id_dict[reqs_path + self.req_split + case['title']] = req_id
                if case['summary'] != '':
                    sm = self.add_child_node(tc, self.req_tag['sm'])
                    self.add_cdata(sm, case['summary'])
                if req_type == '功能':
                    for i in case['reqband']:
                        for j in self.req_id_dict:
                            if j.endswith(i.split('#')[-1]):
                                rel = self.add_child_node(ts, 'relation')
                                source = self.add_child_node(rel, 'source')
                                source.text = self.req_id_dict[j]
                                des  = self.add_child_node(rel, 'destination')
                                des.text = req_id
                                sd_type = self.add_child_node(rel, 'type')
                                sd_type.text = str(2)
        if "suites" in in_dict.keys() and in_dict['suites'] != []:
            for suite in in_dict['suites']:
                if suite['title'] == '功能':
                    req_type = '功能'
                root_id = reqs_id + "." + str(id_count)
                id_count += 1
                self.traverse_req(suite, ts, root_id, req_type)

    def generate_req(self, req_dict, root_id):
        req_root = self.init_node(self.req_tag['root'])
        self.traverse_req(req_dict, req_root, root_id)
        file_name = "req_" + req_dict['title'] + ".xml"
        self.write_xml(req_root, file_name)
        print("create " + file_name)

    def traverse_case(self, in_dict, node = ''):
        if node == '':
            ts = self.init_node(self.case_tag['ts'], attr = {"name":in_dict['title']})
        else:
            ts = self.add_child_node(node, self.case_tag['ts'], attr = {"name":in_dict['title']})
        if "detail" in in_dict.keys() and in_dict['detail'] != '':
            dt = self.add_child_node(ts, self.case_tag['dt'])
            self.add_cdata(dt, in_dict['detail'])
        if "cases" in in_dict.keys() and in_dict['cases'] != []:
            for case in in_dict['cases']:
                tc = self.add_child_node(ts, self.case_tag['tc'], attr = {
                    "name":case['title']
                    })
                if case['preconditions'] != '':
                    pc = self.add_child_node(tc, self.case_tag['pc'])
                    self.add_cdata(pc, case['preconditions'])
                if case['summary'] != '':
                    sm = self.add_child_node(tc, self.case_tag['sm'])
                    self.add_cdata(sm, case['summary'])
                if case['execution_type'] != '':
                    et = self.add_child_node(tc, self.case_tag['et'])
                    self.add_cdata(et, case['execution_type'])
                if case['importance'] != '':
                    ip = self.add_child_node(tc, self.case_tag['ip'])
                    self.add_cdata(ip, case['importance'])
                if case['step'] != []:
                    sts = self.add_child_node(tc, self.case_tag['sts'])
                    for step in case['step']:
                        st = self.add_child_node(sts, self.case_tag['st'])
                        sn = self.add_child_node(st, self.case_tag['sn'])
                        self.add_cdata(sn, step['step_number'])
                        ac = self.add_child_node(st, self.case_tag['ac'])
                        self.add_cdata(ac, step['action'])
                        ep = self.add_child_node(st, self.case_tag['ep'])
                        self.add_cdata(ep, step['expect'])
                        et = self.add_child_node(st, self.case_tag['et'])
                        self.add_cdata(et, step['execution_type'])
                if case['custom_field'] != []:
                    cfs = self.add_child_node(tc, self.case_tag['cfs'])
                    for custom in case['custom_field']:
                        cf = self.add_child_node(cfs, self.case_tag['cf'])
                        nm = self.add_child_node(cf, self.case_tag['nm'])
                        self.add_cdata(nm, custom['name'])
                        val = self.add_child_node(cf, self.case_tag['val'])
                        self.add_cdata(val, custom['value'])
                if 'keywords' in case and case['keywords'] != []:
                    kws = self.add_child_node(tc, self.case_tag['kws'])
                    for keyword in case['keywords']:
                        kw = self.add_child_node(kws, self.case_tag['kw'], attr = {
                            "name":keyword
                            })
                if 'reqband' in case and case['reqband'] != []:
                    reqs = self.add_child_node(tc, self.req_tag['reqs'])
                    for i in case['reqband']:
                        req_id = ''
                        for k, v in self.req_id_dict.items():
                            if k.endswith(i):
                                req_id = v
                                break
                        req = self.add_child_node(reqs, self.req_tag['rq'])
                        did = self.add_child_node(req, self.req_tag['did'])
                        self.add_cdata(did, req_id)
                        rqt = self.add_child_node(req, self.req_tag['rqt'])
                        self.add_cdata(rqt, i.split(self.req_split)[-1])
        if "suites" in in_dict.keys() and in_dict['suites'] != []:
            for suite in in_dict['suites']:
                self.traverse_case(suite, ts)
        return ts

    def generate_case(self, case_dict):
        case_root = self.traverse_case(case_dict)
        file_name = "case_" + case_dict['title'] + ".xml"
        self.write_xml(case_root, file_name)
        print("create " + file_name)

if __name__ == "__main__":
    lt = LibTestlinkxml()
    print(lt.init_node('testsuite',{"name" : "test"}))
