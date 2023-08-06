# -*- coding: utf-8 -*-

import sys
import os
import re


class LibMarkdown():
    def __init__(self, obs_type = 'chiptest'):
        self.obs_type = obs_type

    def init_lib(self):
        if self.obs_type == 'chiptest':
            return ChipTestLib()
        elif self.obs_type == 'gxtest':
            return GxTestLib()

class ChipTestLib():
    def __init__(self):
        pass

    def read_markdown(self, markdown_path):
        with open(markdown_path) as fd:
            context = fd.read()
            return context

    def get_paragraph(self, source, title, level = ''):
        paragraph = ''
        start = 0
        for line in source.split('\n'):
            if not line:
                continue
            if line == '#'*level + ' ' + title:
                start = 1
                continue
            if start:
                if line[0] == '#' and line.split(' ')[0].count('#') <= level:
                    start = 0
                    break
                paragraph += line + '\n'
        return paragraph

    def get_title_list(self, source, level = ''):
        title_list = []
        for line in source.split('\n'):
            if not line:
                continue
            if line[0] == '#' and line.split(' ')[0].count('#') == level:
                title = line[level+1:]
                title_list.append(title)
        return title_list

    def get_summary(self, source):
        summary = self.get_paragraph(source, '摘要', 2)
        return summary

    def get_precondition(self, source):
        precondition = self.get_paragraph(source, '前提', 2)
        return precondition

    def get_importance(self, source):
        return 2

    def get_execution_type(self, source):
        return 2

    def get_custom_fields(self, source):
        custom_fields = []
        custom_msg = re.findall('#.*/.*', source)
        for i in custom_msg:
            if i.strip('#')[0] != ' ' and i.count("#") == 1:
                msg = i.strip('#').split('/')
                custom = {
                        "name" : msg[0],
                        "value" : msg[1]}
                custom_fields.append(custom)
        return custom_fields

    def init_step(self):
        step_dict = {
            "step_number" : "", #步骤序号
            "action" : "", #具体动作
            "expect" : "", #期望结果
            "execution_type" : "", #手动/自动
        }
        return step_dict

    def get_steps(self, source, execution_type = 2):
        steps = []
        step_text = self.get_paragraph(source, '步骤', 2)
        count = -1 #第一行表头,第二行分隔栏,第三行才是正式步骤, 计数 -1, 0, 1, 2 ...
        for i in step_text.split('\n'):
            if i.startswith('|') and i.endswith('|'):
                msg = i.strip('|').split('|')
                step = self.init_step()
                step['step_number'] = count
                step['action'] = msg[0].strip(' ')
                step['expect'] = msg[1].strip(' ')
                if msg[2].strip(' ') == "自动":
                    step['execution_type'] = 2
                elif msg[2].strip(' ') == "手动":
                    step['execution_type'] = 1
                count += 1
                steps.append(step)
        return steps[2:]

    def get_reqband(self, source):
        reqs = []
        req_text = self.get_paragraph(source, '功能', 2)
        for i in req_text.split('\n'):
            if not i:
                continue
            tmp = re.findall('\[\[(.*)\]\]', i)
            if tmp != []:
                req = tmp[0]
                reqs.append(req)
        return reqs

    def get_keywords(self, source):
        keywords = []
        msg_text = self.get_paragraph(source, '属性', 2)
        if not msg_text:
            return keywords
        flag_list = ['-', '*']
        flag = msg_text[0]
        if flag not in flag_list:
            return keywords
        data = msg_text.strip(flag + ' ').split('\n' + flag + ' ')
        for i in data:
            if i.startswith('关键字'):
                msg = i.split(flag + ' ')
                if len(msg) <= 1:
                    break
                for key in msg[1:]:
                    keywords.append(key.strip('#\n\t '))
        return keywords


class GxTestLib(ChipTestLib):
    def __init__(self):
        self.flag_list = ['-', '*']
        pass

    def get_summary(self, source):
        summary = ''
        msg_text = self.get_paragraph(source, '摘要', 2)
        if not msg_text:
            return summary
        flag = msg_text[0]
        if flag not in self.flag_list:
            return summary
        data = msg_text.strip(flag + ' ').split('\n' + flag + ' ')
        for i in data:
            msg = i.split(flag + ' ')
            summary += '\n' + msg[0].strip(' \n\t') + ':\n' + flag + ' ' + msg[1] + '\n'
        return summary

    def get_custom_fields(self, source):
        custom_fields = []
        msg_text = self.get_paragraph(source, '属性', 2)
        if not msg_text:
            return custom_fields
        flag = msg_text[0]
        if flag not in self.flag_list:
            return custom_fields
        data = msg_text.strip(flag + ' ').split('\n' + flag + ' ')
        for i in data:
            if i.startswith('关键字'):
                continue
            if i.startswith('优先级'):
                continue
            if i.startswith('执行方式'):
                continue
            msg = i.split(flag + ' ')
            custom = {
                    "name" : msg[0].strip(' \n\t'),
                    "value" : msg[1]
                    }
            custom_fields.append(custom)
        return custom_fields

    def get_importance(self, source):
        importance = 2
        msg_text = self.get_paragraph(source, '属性', 2)
        if not msg_text:
            return importance
        flag = msg_text[0]
        if flag not in self.flag_list:
            return importance
        data = msg_text.strip(flag + ' ').split('\n' + flag + ' ')
        for i in data:
            if i.startswith('优先级'):
                msg = i.split(flag + ' ')
                level = msg[1].strip(' \n\t').lower()
                if level in ['high', '高']:
                    importance = 3
                elif level in ['low', '低']:
                    importance = 1
        return importance

    def get_execution_type(self, source):
        execution_type = 2
        msg_text = self.get_paragraph(source, '属性', 2)
        if not msg_text:
            return execution_type
        flag = msg_text[0]
        if flag not in self.flag_list:
            return execution_type
        data = msg_text.strip(flag + ' ').split('\n' + flag + ' ')
        for i in data:
            if i.startswith('执行方式'):
                msg = i.split(flag + ' ')
                level = msg[1].strip(' \n\t').lower()
                if level in ['auto', '自动']:
                    execution_type = 2
                elif level in ['manual', '手动']:
                    execution_type = 1
        return execution_type

    def get_steps(self, source, execution_type = 2):
        steps = []
        step_text = self.get_paragraph(source, '步骤', 2)
        if not step_text:
            return steps
        count = 1
        flag_list = ['-', '*']
        flag = step_text[0]
        if flag not in self.flag_list:
            return steps
        data = step_text.strip(flag + ' ').split('\n' + flag + ' ')
        for i in data:
            msg = i.split(flag + ' ')
            step = self.init_step()
            step['step_number'] = count
            step['action'] = msg[0].strip(' \n\t')
            if len(msg) == 2:
                step['expect'] = msg[1].strip(' \n\t')
            step['execution_type'] = execution_type
            count += 1
            steps.append(step)
        return steps

    #def get_reqband(self, source):
    #    reqs = []
    #    req_text = self.get_paragraph(source, '覆盖范围', 2)
    #    for i in req_text.split('\n'):
    #        if not i:
    #            continue
    #        tmp = re.findall('\[\[(.*)\]\]', i)
    #        if tmp != []:
    #            req = tmp[0]
    #            reqs.append(req)
    #    return reqs


if __name__ == "__main__":
    lm = LibMarkdown()
    md_path = 'example_obs/功能/支持BootCode解密.md'
    source = lm.read_markdown(md_path)
    print(lm.get_paragraph(source, '功能描述', 2))
    print(lm.get_title_list(source, 2))
