# -*- coding: utf-8 -*-

import sys
import os
import re
import argparse
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import libmarkdown
import libtestlinkxml

class ObisidianToTestlink():
    def __init__(self, obs_dir, req_id, small, obs_type):
        self.lm = libmarkdown.LibMarkdown(obs_type).init_lib()
        self.lt = libtestlinkxml.LibTestlinkxml(small)
        self.obs_dir = obs_dir
        if obs_dir.endswith('/'):
            self.obs_name = os.path.basename(os.path.dirname(obs_dir))
        else:
            self.obs_name = os.path.basename(obs_dir)
        self.req_id = req_id
        self.obs_type = obs_type

    def init_case(self):
        case = {
                'title':'',
                'summary':'',
                'preconditions':'',
                'importance':'',
                'execution_type':2,
                'custom_field':[],
                'step':[],
                'reqband':[],
                'keywords':[]
                }
        return case

    def init_suite(self):
        suite = {
                'title':'',
                'detail':'',
                'suites':[],
                'cases':[]
                }
        return suite

    def traverse_function(self, md_dir, suite):
        for i in os.listdir(md_dir):
            if i == '功能.md':
                continue
            path = os.path.join(md_dir, i)
            if os.path.isdir(path):
                sub_suite = self.init_suite()
                sub_suite['title'] = i
                suite['suites'].append(sub_suite)
                self.traverse_function(path, sub_suite)
            elif i[-3:].lower() == '.md':
                case = self.init_case()
                case['title'] = i[:-3]
                md_text = self.lm.read_markdown(path)
                case['summary'] = self.lm.get_paragraph(md_text, '功能描述', 2)
                bandmsg = self.lm.get_paragraph(md_text, '功能步骤', 2)
                band_list = re.findall('\[\[(.*)\]\]', bandmsg)
                case['reqband'] = band_list
                suite['cases'].append(case)

    def get_function(self):
        function_dir = os.path.join(self.obs_dir, '功能')
        suite = self.init_suite()
        suite['title'] = '功能'
        self.traverse_function(function_dir, suite)
        return suite

    def traverse_feature(self, md_dir, suite):
        for i in os.listdir(md_dir):
            if i == '特性.md':
                continue
            path = os.path.join(md_dir, i)
            if os.path.isdir(path):
                sub_suite = self.init_suite()
                sub_suite['title'] = i
                suite['suites'].append(sub_suite)
                self.traverse_feature(path, sub_suite)
            elif i[-3:].lower() == '.md':
                #case = self.init_case()
                #case['title'] = i[:-3]
                #md_text = self.lm.read_markdown(path)
                #case['summary'] = '\n'.join(self.lm.get_title_list(md_text, 2))
                #suite['cases'].append(case)
                md_text = self.lm.read_markdown(path)
                first_title = self.lm.get_title_list(md_text, 1)
                if len(first_title) > 0:
                    sub_suite = self.init_suite()
                    sub_suite['title'] = first_title[0]
                    suite['suites'].append(sub_suite)
                    suite = sub_suite
                second_title = self.lm.get_title_list(md_text, 2)
                for feature in second_title:
                    case = self.init_case()
                    case['title'] = feature
                    feature_summary = self.lm.get_paragraph(md_text, feature, 2)
                    feature_summary = re.sub('!\[\[.*\]\]\\n', '', feature_summary)
                    if feature_summary:
                        case['summary'] = feature_summary 
                    suite['cases'].append(case)


    def get_feature(self):
        feature_dir = os.path.join(self.obs_dir, '特性')
        suite = self.init_suite()
        suite['title'] = '特性'
        self.traverse_feature(feature_dir, suite)
        return suite

    def traverse_testcase(self, md_dir, suite):
        for i in os.listdir(md_dir):
            if i == '用例.md':
                continue
            path = os.path.join(md_dir, i)
            if os.path.isdir(path):
                sub_suite = self.init_suite()
                sub_suite['title'] = i
                suite['suites'].append(sub_suite)
                self.traverse_testcase(path, sub_suite)
            elif i[-3:].lower() == '.md':
                case = self.init_case()
                case['title'] = i[:-3]
                md_text = self.lm.read_markdown(path)
                case['summary'] = self.lm.get_summary(md_text)
                case['preconditions'] = self.lm.get_precondition(md_text)
                case['importance'] = self.lm.get_importance(md_text)
                case['execution_type'] = self.lm.get_execution_type(md_text)
                case['step'] = self.lm.get_steps(md_text, case['execution_type'])
                case['custom_field'] = self.lm.get_custom_fields(md_text)
                case['reqband'] = self.lm.get_reqband(md_text)
                case['keywords'] = self.lm.get_keywords(md_text)
                suite['cases'].append(case)

    def get_testcase(self, case_root):
        case_dir = os.path.join(self.obs_dir, '用例')
        self.traverse_testcase(case_dir, case_root)


    def chiptest_start(self):
        req_root = self.init_suite()
        req_root['title'] = self.obs_name
        req_root['suites'].append(self.get_feature())
        req_root['suites'].append(self.get_function())

        case_root = self.init_suite()
        case_root['title'] = self.obs_name
        self.get_testcase(case_root)

        if self.req_id:
            self.lt.generate_req(req_root, self.req_id)
        self.lt.generate_case(case_root)

    def gxtest_start(self):
        case_root = self.init_suite()
        case_root['title'] = self.obs_name
        self.get_testcase(case_root)
        self.lt.generate_case(case_root)

    def start(self):
        if self.obs_type == 'chiptest':
            self.chiptest_start()
        if self.obs_type == 'gxtest':
            self.gxtest_start()

def main():
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument('-d', dest='obs_dir',
            help='指定obisidian文档目录, 必填')
    parser.add_argument('-i', dest='req_id',
            help='指定需求根id, 若不生成需求，可不填')
    parser.add_argument('-t', dest='type', default = 'gxtest',
            help='指定用例类型，chiptest/gxtest')
    parser.add_argument('-s', '--small', dest='small', action='store_const', const=True,
            default=False,
            help='使xml文件大小减小, 但降低可读性，一般不加')
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    obs_dir = args.obs_dir
    req_id = args.req_id
    small = args.small
    obs_type = args.type

    ot = ObisidianToTestlink(obs_dir, req_id, small, obs_type)
    ot.start()

if __name__ == "__main__":
    main()
