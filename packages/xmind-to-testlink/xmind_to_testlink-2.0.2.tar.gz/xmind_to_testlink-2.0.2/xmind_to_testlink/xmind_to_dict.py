# -*- coding: utf-8 -*-

import os
import sys
import json
import copy
from zipfile import  ZipFile
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import preprocess
import chipcase_restructure

class XmindToDict(object):
    def __init__(self, xmind_type = "case"):
        '''
        type = "case" 按用例设计规则解析xmind文件
        type = "req" 按需求分析规则解析xmind文件
        '''
        self.type = xmind_type
        self.save_req = []
        self.branch_start = 0
        self.root_node_name = ''
        self.repeat_req = ''
        self.case_count = 1

    def open_xmind(self, file_path):
        '''
        打开xmind文件，返回其中的内容
        '''
        target_file = "content.json"
        with ZipFile(file_path) as xmind:
            for f in xmind.namelist():
                if f == target_file:
                    return (xmind.open(f).read().decode('utf-8'))

    def create_suite(self, name, suite_detail = ''):
        suite = {
                'title':'',
                'detail':'',
                'suites':[],
                'cases':[]
                }
        suite['title'] = name.strip(" .,").replace(' ','')
        suite['detail'] = suite_detail
        return suite
    
    def get_summery(self, in_dict):
        return in_dict['plain']['content']
    
    def get_custom_fields(self, save_custom, in_data):
        old_custom = copy.deepcopy(save_custom)
        for attach in in_data['children']['attached']:
            find = 0
            if isinstance(attach, dict):
                if "children" in attach and attach['children'] != {}:
                    if len(attach['children']['attached']) == 1:
                        new_vs = attach['children']['attached'][0]['title']
                    else:
                        multi_list = []
                        for multi_value in attach['children']['attached']:
                            multi_list.append(multi_value['title'])
                        new_vs = '|'.join(multi_list)
                else:
                    print("Warning: 属性：" + attach['title']  + " 未添加属性值")
                    new_vs = ""
                ol = len(old_custom)
                if ol >= 1:
                    for i in range(ol):
                        for k,v in old_custom[i].items():
                            if k == attach['title']:
                                old_v = old_custom[i][k].split("|")
                                new_v = new_vs.split("|")
                                value = list(set(old_v + new_v))
                                value.sort()
                                if '' in value:
                                    value.remove('')
                                old_custom[i][k] = "|".join(value)
                                find = 1
                    if not find:
                        custom = {}
                        custom[attach['title']] = new_vs
                        old_custom.append(custom)
                else:
                    old_custom = []
                    custom = {}
                    custom[attach['title']] = new_vs
                    old_custom.append(custom)
        return old_custom
    
    def get_steps(self, in_data):
        steps = []
        for attach in in_data['children']['attached']:
            if isinstance(attach, dict):
                step = {}
                step['action'] = attach['title']
                if "children" in attach and attach['children'] != {}:
                    step['expect'] = attach['children']['attached'][0]['title']
                else:
                    step['expect'] = ''
                if "notes" in attach.keys() and attach['notes'] != '':
                    step['notes'] = attach["notes"]["plain"]["content"]
                #if "children" in attach and attach['children'] != {}:
                #    step[attach['title']] = attach['children']['attached'][0]['title']
                #else:
                #    step[attach['title']] = ""
                steps.append(step)
        return steps
    
    def get_execution_type(self, in_data):
        if in_data == "自动" or in_data == 'auto':
            return 2
        elif in_data == "手动" or in_data == 'manual':
            return 1
        else:
            return 2

    def _get_tf_name(self, summary):
        if summary.find('gxtestfilename:') >= 0:
            msg = summary.split('\n')
            for line in msg :
                if line.startswith('gxtestfilename:'):
                    return line
        return ''

    def _add_summary(self, in_data):
        summary = ''
        if not in_data['title'].startswith('[[参数]]'):
            summary = '<strong>[[brief]]</strong>' + '\n' + in_data['title'] + '\n'
        if 'notes' in in_data.keys():
            case_summary = in_data['notes']['plain']['content']
            new_tf_name = self._get_tf_name(case_summary)
            if new_tf_name != '':
                #summary = '<strong>' + new_tf_name.split(':')[0] + '</strong>' + '\n' + \
                #        + new_tf_name.split(':')[1] + summary
                summary = new_tf_name + '\n' + summary

        if "children" in in_data.keys() and in_data['children'] != {}:
            if "attached" in in_data['children']:
                for attach in in_data['children']['attached']:
                    #print(attach)
                    if isinstance(attach, dict):
                        if attach['title'] == "属性" or attach['title'] == "步骤" \
                                or attach['title'] == "等级":
                            continue
                        else:
                            #summary += self._add_summary(attach)
                            try:
                                summary += '<strong>[[' + attach['title'] + ']]</strong>' + '\n' + \
                                        attach['children']['attached'][0]['title'] +  '\n'
                            except:
                                pass
        return summary


    def get_summary(self, attach):
        summary = ''
        if len(attach['children']['attached']) != 2:
            return ''
        target = attach['children']['attached'][0]
        expect = attach['children']['attached'][1]
        summary = '\n' + target['title'] + ':\n'
        if "children" in target and target['children'] != {}:
            summary += '- ' + target['children']['attached'][0]['title'] + '\n'
        summary += '\n' + expect['title'] + ':\n'
        if "children" in expect and expect['children'] != {}:
            summary += '- ' + expect['children']['attached'][0]['title'] + '\n'
        summary += '\n'
        return summary


    def create_case(self, in_data, pre_dict, num, req_spec, req, save_custom = '', repeat_argv = '', is_case = 1, father = '', tf_name = ''):
        case = {
                'title':'',
                'summary':'',
                'preconditions':'',
                'importance':'',
                'execution_type':2,
                'custom_field':[],
                'step':[],
                'casename':'',
                'keywords':[],
                #'reqband':[],
                }
        case['custom_field'] = copy.deepcopy(save_custom)
        new_custom = 0
        if "title" in in_data.keys():
            title_msg = in_data['title'].strip(" .,").replace(' ','')
            case['title'] = in_data['title']
            if len(in_data['title']) >= 100:
                print('ERROR [ case_title length >= 100 ]:' + in_data['title'])
                sys.exit()
        if "children" in in_data.keys() and in_data['children'] != {}:
            if "attached" in in_data['children']:
                for attach in in_data['children']['attached']:
                    if isinstance(attach, dict):
                        if attach['title'] == "用例名" and "children" in attach \
                                and attach['children'] != {}:
                            case['casename'] = attach['children']['attached'][0]['title']
                        if attach['title'] == "摘要" and "children" in attach \
                                and attach['children'] != {}:
                                    case['summary'] = self.get_summary(attach)
                        if attach['title'] == "前提" and "children" in attach \
                                and attach['children'] != {}:
                            case['preconditions'] = attach['children']['attached'][0]['title']
                        if attach['title'] == "属性" and "children" in attach \
                                and attach['children'] != {}:
                            new_custom = 1
                            case['custom_field'] = self.get_custom_fields(save_custom, attach)
                            copy_custom = copy.deepcopy(case['custom_field'])
                            for tmp_custom in copy_custom:
                                if "执行方式" in tmp_custom:
                                    case['execution_type'] = \
                                            self.get_execution_type(tmp_custom['执行方式'])
                                    case['custom_field'].remove(tmp_custom)
                                if "等级" in tmp_custom:
                                    if tmp_custom['等级'] == 'high':
                                        case['importance'] = 3
                                    elif tmp_custom['等级'] == 'low':
                                        case['importance'] = 1
                                    case['custom_field'].remove(tmp_custom)
                                elif "优先级" in tmp_custom:
                                    if tmp_custom['优先级'] == 'high':
                                        case['importance'] = 3
                                    elif tmp_custom['优先级'] == 'low':
                                        case['importance'] = 1
                                    case['custom_field'].remove(tmp_custom)
                                if "关键字" in tmp_custom:
                                    case['keywords'] = tmp_custom['关键字'].split('|')
                                    case['custom_field'].remove(tmp_custom)
                        elif attach['title'] == "步骤" and "children" in attach \
                                and attach['children'] != {}:
                            case['step'] = self.get_steps(attach)
                if not new_custom:
                    copy_custom = copy.deepcopy(case['custom_field'])
                    for tmp_custom in copy_custom:
                        if "执行方式" in tmp_custom:
                            case['execution_type'] = \
                                    self.get_execution_type(tmp_custom['执行方式'])
                            case['custom_field'].remove(tmp_custom)
                        if "等级" in tmp_custom:
                            if tmp_custom['等级'] == 'high':
                                case['importance'] = 3
                            elif tmp_custom['等级'] == 'low':
                                case['importance'] = 1
                            case['custom_field'].remove(tmp_custom)
        #print(">>>>>>>>>>>>>>>>>>>>")
        #print(case)
        #print(case['importance'])
        #print(">>>>>>>>>>>>>>>>>>>>")
        return case

    def have_case(self, in_data):
        msg = "\'title\': \'用例\'"
        if str(in_data).find(msg) >= 0:
            return 1
        else:
            return 0

    def have_req(self, in_data):
        msg = "\'title\': \'需求分析\'"
        if str(in_data).find(msg) >= 0:
            return 1
        else:
            return 0
    

    def is_case(self, in_data):
        case = 0
        for branch in in_data['children']['attached']:
            if branch['title'] != "属性" and branch['title'] != "步骤" \
                    and branch['title'] != "用例名" and branch['title'] != "摘要" \
                    and branch['title'] != "前提" and branch['title'] != "需求":
                case = 0
                break
            else:
                case = 1
        return case
        #case = 0 
        #if 'notes' in in_data.keys():
        #    suite_detail = in_data["notes"]["plain"]["content"]
        #    for i  in suite_detail.split('\n'):
        #        if i.startswith('[[') and i.endswith(']]'):
        #            case = 1
        #            break
        #return case
    
    def check_suite_or_case(self, in_data):
        if "children" not in in_data.keys() or in_data['children'] == {} \
            or self.is_case(in_data):
                return "case"
        else:
                return "suite"
        #if self.is_case(in_data):
        #    return "case"
        #else:
        #    return  "suite"

    def is_req(self, in_data):
        have_other_br = 0
        for branch in in_data['children']['attached']:
            if branch['title'] != "用例":
                have_other_br = 1
                break
        if have_other_br:
            return 0
        else:
            return 1

    def check_reqs_or_req(self, in_data):
        if "children" not in in_data.keys() or in_data['children'] == {}\
                or self.is_req(in_data):
                    return "req"
        else:
            return  "reqs"
    
    def get_req_dict(self, in_data, out_dict, start = 0):
        if not self.have_case(in_data) and start == 0:
            return 0
        else:
            if "title" in in_data.keys():
                in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                if in_data['title'] == "用例":
                    start = 1
                    return 0
                elif in_data['title'] != "用例":
                    sc = self.check_reqs_or_req(in_data)
                    if sc == "req":
                        case = self.create_case(in_data, pre_dict = {}, num = 0, req_spec = '', req = '')
                        out_dict['cases'].append(case)
                        return 1
                    elif sc == "reqs":
                        suite_detail = ""
                        if "notes" in in_data.keys():
                            suite_detail = in_data["notes"]["plain"]["content"]
                        suite = self.create_suite(in_data['title'], suite_detail)
                        out_dict['suites'].append(suite)
                        out_dict = suite
            if "notes" in in_data.keys():
                #需求的范围
                suite_detail = in_data["notes"]["plain"]["content"]
            if "children" in in_data.keys():
                if "attached" in in_data['children']:
                    #递归，遍历嵌套的节点
                    for count in range(len(in_data['children']['attached'])):
                        attach = in_data['children']['attached'][count]
                        if isinstance(attach, dict):
                            self.get_req_dict(attach, out_dict, start)

    def next_is_case(self, br_list):
        ret = 0
        for br in br_list:
            if br['title'] == "用例":
                ret = 1
                break
        return ret

    def get_chip_req_dict(self, in_data, out_dict, save_custom = [], start = 0):
        if not self.have_case(in_data) and start == 0:
            return 0
        else:
            if "title" in in_data.keys():
                in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                if in_data['title'] == "用例":
                    return 0
                elif in_data['title'] != "用例":
                    sc = self.check_reqs_or_req(in_data)
                    if sc == "req":
                        case = self.create_case(in_data, pre_dict = {}, num = 0, \
                                req_spec = '', req = '', \
                                save_custom = save_custom, is_case = 0)
                        out_dict['cases'].append(case)
                        return 1
                    elif sc == "reqs":
                        suite_detail = ""
                        if "notes" in in_data.keys():
                            suite_detail = in_data["notes"]["plain"]["content"]
                        suite = self.create_suite(in_data['title'], suite_detail)
                        out_dict['suites'].append(suite)
                        out_dict = suite
            if "notes" in in_data.keys():
                #需求的范围
                suite_detail = in_data["notes"]["plain"]["content"]
            if "children" in in_data.keys():
                if "attached" in in_data['children']:
                    #递归，遍历嵌套的节点
                    save_custom = self.check_save_custom(save_custom, \
                            in_data['children']['attached'])
                    if self.next_is_case(in_data['children']['attached']):
                        start = 1
                    for count in range(len(in_data['children']['attached'])):
                        attach = in_data['children']['attached'][count]
                        self.get_chip_req_dict(attach, out_dict, save_custom, start)


    def parse_xmind(self, in_data, out_dict, start = 0, pre_dict = {}, count = 0, req_spec = '', req = '', save_custom = [], repeat_argv = '', father = '', tf_name = ''):
        if "title" in in_data.keys():
            if in_data['title'] == "属性":
                return
            if in_data['title'] == "用例":
                start = 1
                father = in_data['title']
            elif in_data['title'] != "用例":
                #if father == '用例':
                #    sc = 'suite' 
                #else:
                sc = self.check_suite_or_case(in_data)
                #print(in_data['title'], sc, father)
                if sc == "case":
                    if in_data['title'].find("xmindrepeat-") >= 0:
                        in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                    case = self.create_case(in_data, pre_dict, count, req_spec, req, save_custom, repeat_argv, father = father, tf_name = tf_name)
                    out_dict['cases'].append(case)
                    #import pdb; pdb.set_trace()
                    return 1
                elif sc == "suite":
                    if in_data['title'].find("xmindrepeat-") >= 0:
                        in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                    father = in_data['title']
                    if len(in_data['title']) >= 100:
                        print('Warning :' + in_data['title'])
                    repeat_argv = repeat_argv + in_data['title'] + "~"
                    #req_spec 和 req 给需求绑定用
                    if start == 0:
                        if req_spec == '':
                            req_spec = in_data['title']
                        elif req == '':
                            req = req_spec + "/" + in_data['title']
                        else:
                            req_spec = req.split('/')[-1]
                            req = req + "/" + in_data['title']
                    #count 和pre_dict 给用例前提用
                    count = 0
                    pre_dict = {}
                    suite_detail = ""
                    if "notes" in in_data.keys():
                        suite_detail = in_data["notes"]["plain"]["content"]
                    new_tf_name = self._get_tf_name(suite_detail)
                    if new_tf_name != '':
                        tf_name = new_tf_name
                    suite = self.create_suite(in_data['title'], suite_detail)
                    out_dict['suites'].append(suite)
                    out_dict = suite
        if "notes" in in_data.keys():
            #测试集的摘要
            suite_detail = in_data["notes"]["plain"]["content"]
        if "summaries" in in_data.keys():
            #测试用例的前提的位置
            for pre in in_data["summaries"]:
                pre_dict[pre['range'].split(',')[0].split("(")[1]] = pre['topicId']
        if "children" in in_data.keys():
            if "summary" in in_data["children"]:
                #测试用例的前提
                for pre in in_data["children"]['summary']:
                    for k,v in pre_dict.items():
                        if pre['id'] == v:
                            pre_dict[k] = pre['title']
            if "attached" in in_data['children']:
                #检查继承属性
                save_custom = self.check_save_custom(save_custom, in_data['children']['attached'])
                #递归，遍历嵌套的节点
                for count in range(len(in_data['children']['attached'])):
                    attach = in_data['children']['attached'][count]
                    if isinstance(attach, dict):
                        if self.type == "chipreq":
                            if not self.have_case(attach):
                                self.get_dict(attach, out_dict, start, pre_dict, count, req_spec, req, save_custom)
                            else:
                                continue
                        else:
                            self.get_dict(attach, out_dict, start, pre_dict, count, req_spec, req, save_custom, repeat_argv, father, tf_name)


    def get_dict(self, in_data, out_dict, start = 0, pre_dict = {}, count = 0, req_spec = '', req = '', save_custom = [], repeat_argv = '', father = '', tf_name = ''):
        if self.type == "case":
            if not self.have_case(in_data) and start == 0:
                return 0
            else:
                self.parse_xmind(in_data, out_dict, start, pre_dict, count, req_spec, req, save_custom, father = father, tf_name = tf_name)
        elif self.type == "req":
            self.parse_xmind(in_data, out_dict, start, pre_dict, count, req_spec, req, save_custom)
        elif self.type == "chipreq":
            self.parse_xmind(in_data, out_dict, start, pre_dict, count, req_spec, req, save_custom)
        elif self.type == "chipcase" or self.type == "checkxmind":
            if not self.have_case(in_data) and start == 0:
                return 0
            else:
            #    #self.parse_xmind(in_data, out_dict, start, pre_dict, count, req_spec, req, save_custom, repeat_argv)
                self.root_node_name = in_data['title']
                self.get_function_dict(in_data, out_dict, start, pre_dict, count, req_spec, req, save_custom, repeat_argv)

    def check_save_custom(self, old_custom, in_data):
        for attach in in_data: 
            if "title" in attach.keys() and attach['title'] == "属性":
                old_custom = self.get_custom_fields(old_custom, attach)
        return old_custom
    
    def get_root(self, in_dict):
        root_name = in_dict[0]['title']
        return root_name

    def get_branch_dict(self, in_data, out_dict, branch_name, start = 0, pre_dict = {}, count = 0, req_spec = '', req = '', save_custom = [], repeat_argv = '', father = ''):
        if "title" in in_data.keys():
            sc = self.case_check_suite_or_case(in_data, father)
            if sc == "case":
                if in_data['title'].find("xmindrepeat-") >= 0:
                    in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                #case = self.create_case(in_data, pre_dict, count, req_spec, req, save_custom, repeat_argv)
                case = self.create_base_case(in_data, pre_dict, count, req_spec, req)
                out_dict['cases'].append(case)
                return 1
            elif sc == "suite":
                father = in_data['title']
                if in_data['title'].find("xmindrepeat-") >= 0:
                    in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                    repeat_argv = repeat_argv + in_data['title'] + "~"
                suite_detail = ""
                if "notes" in in_data.keys():
                    suite_detail = in_data["notes"]["plain"]["content"]
                suite = self.create_suite(in_data['title'], suite_detail)
                out_dict['suites'].append(suite)
                out_dict = suite
        if "notes" in in_data.keys():
            #测试集的摘要
            suite_detail = in_data["notes"]["plain"]["content"]
        if "children" in in_data.keys():
            if "attached" in in_data['children']:
                #递归，遍历嵌套的节点
                for count in range(len(in_data['children']['attached'])):
                    attach = in_data['children']['attached'][count]
                    if self.branch_start:
                        self.get_branch_dict(attach, out_dict, branch_name, start, pre_dict, count, req_spec, req, save_custom, repeat_argv, father)
                    elif attach['title'] == branch_name:
                        self.branch_start = 1
                        self.get_branch_dict(attach, out_dict, branch_name, start, pre_dict, count, req_spec, req, save_custom, repeat_argv, father)
                        self.branch_start = 0

    def get_function_dict(self, in_data, out_dict, start = 0, pre_dict = {}, count = 0, \
            req_spec = '', req = '', save_custom = [], repeat_argv = '', right_br = 0):
        if "title" in in_data.keys():
            if in_data['title'] == "属性":
                return
            if in_data['title'] == "用例":
                start = 1
            elif in_data['title'] != "用例":
                sc = self.check_suite_or_case(in_data)
                if sc == "case":
                    if in_data['title'].find("xmindrepeat-") >= 0:
                        in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                    case = self.create_case(in_data, pre_dict, count, req_spec, req, \
                            save_custom, repeat_argv)
                    out_dict['cases'].append(case)
                    return 1
                elif sc == "suite":
                    if in_data['title'].find("xmindrepeat-") >= 0:
                        in_data['title'] = in_data['title'].replace("xmindrepeat-",'')
                    repeat_argv = repeat_argv + in_data['title'] + "~"
                    #req_spec 和 req 给需求绑定用
                    if start == 0:
                        if req_spec == '':
                            req_spec = in_data['title']
                        elif req == '':
                            req = req_spec + "/" + in_data['title']
                        else:
                            req_spec = req.split('/')[-1]
                            req = req + "/" + in_data['title']
                    #count 和pre_dict 给用例前提用
                    count = 0
                    pre_dict = {}
                    suite_detail = ""
                    if "notes" in in_data.keys():
                        suite_detail = in_data["notes"]["plain"]["content"]
                    suite = self.create_suite(in_data['title'], suite_detail)
                    out_dict['suites'].append(suite)
                    out_dict = suite
        if "notes" in in_data.keys():
            #测试集的摘要
            suite_detail = in_data["notes"]["plain"]["content"]
        if "summaries" in in_data.keys():
            #测试用例的前提的位置
            for pre in in_data["summaries"]:
                pre_dict[pre['range'].split(',')[0].split("(")[1]] = pre['topicId']
        if "children" in in_data.keys():
            if "summary" in in_data["children"]:
                #测试用例的前提
                for pre in in_data["children"]['summary']:
                    for k,v in pre_dict.items():
                        if pre['id'] == v:
                            pre_dict[k] = pre['title']
            if "attached" in in_data['children']:
                #检查继承属性
                need_clean = 0
                old_save_req = copy.deepcopy(self.save_req)
                save_custom = self.check_save_custom(save_custom, in_data['children']['attached'])
                #if start == 0 and right_br:
                if start == 0 and in_data['title'] != self.root_node_name:
                    self.check_save_req(self.save_req, in_data['children']['attached'], req)
                    if old_save_req != self.save_req:
                        need_clean = 1
                #print("node: ", in_data['title'])
                #递归，遍历嵌套的节点
                for count in range(len(in_data['children']['attached'])):
                    attach = in_data['children']['attached'][count]
                    #print(attach['title'])
                    #if right_br:
                        #attach = in_data['children']['attached'][count]
                    if not self.have_case(attach) and start == 0:
                        continue
                    else:
                        self.get_function_dict(attach, out_dict, start, pre_dict, count, \
                                req_spec, req, save_custom, repeat_argv, right_br)
                    #elif attach['title'] == "功能特性":
                    #    right_br = 1
                    #    self.get_function_dict(attach, out_dict, start, pre_dict, count, \
                    #            req_spec, req, save_custom, repeat_argv, right_br)
                if need_clean:
                    self.save_req = old_save_req

    def check_save_req(self, old_req, in_data, req_path):
        for attach in in_data: 
            if not self.have_case(attach):
                old_req.extend(self.get_save_req(attach, req_path))
        return old_req

    def get_save_req(self, in_data, req_path):
        req_msg = []
        if "children" in in_data.keys():
            if "attached" in in_data['children']:
                for attach in in_data['children']['attached']:
                    req = req_path + "/" + in_data['title']
                    req_msg.extend(self.get_save_req(attach, req))
        elif "children" not in in_data.keys() or in_data['children'] == {}:
            req_spec = req_path.split('/')[-1]
            req = req_path + "/" + in_data['title']
            req_msg.append({req:req_spec})
        return req_msg
            
    def start(self, xmind_file):
        pp = preprocess.PreProcess()
        js_dict = pp.start(xmind_file)
        #js_str = str(self.open_xmind(xmind_file))
        #js_dict = json.loads(js_str)
        root_name = self.get_root(js_dict)
        root_dict = self.create_suite(root_name)
        if self.type == "case" or self.type == "chipcase":
            #仅解析带有“用例”节点的分支
            self.get_dict(js_dict[0]['rootTopic'], root_dict)#得到用例字典
            req_name = self.get_root(js_dict)
            req_dict = self.create_suite(root_name)
            if self.type == "chipcase":
                root_dict = chipcase_restructure.restructure_dict(root_dict)
                self.get_chip_req_dict(js_dict[0]['rootTopic'], req_dict)#得到用例对应的需求字典
            else:
                self.get_req_dict(js_dict[0]['rootTopic'], req_dict)#得到用例对应的需求字典
            return root_dict, req_dict
        elif self.type == "req" or self.type == "chipreq":
            # req,解析所有分支; chipreq，解析不带"用例"字段的分支
            req_name = self.get_root(js_dict)
            req_dict = self.create_suite(root_name)
            self.get_dict(js_dict[0]['rootTopic'], req_dict)#得到需求字典
            return root_dict, req_dict

    def get_register_msg(self, xmind_file):
        if self.type == "checkxmind":
            pp = preprocess.PreProcess()
            js_dict = pp.start(xmind_file)
            root_name = self.get_root(js_dict)

            root_dict = self.create_suite(root_name)
            self.get_branch_dict(js_dict[0]['rootTopic'], root_dict, '功能特性')
            #print(root_dict)
            register_dict = self.create_suite(root_name)
            self.get_branch_dict(js_dict[0]['rootTopic'], register_dict, 'register')
            #print(register_dict)

            return root_dict, register_dict

    def get_case_req_dict(self, xmind_file):
        if self.type == "case_req":
            pp = preprocess.PreProcess()
            js_dict = pp.start(xmind_file)
            root_name = self.get_root(js_dict)
            req_dict = self.create_suite(root_name)
            self.parse_req_xmind(js_dict[0]['rootTopic'], req_dict)
            case_dict = self.create_suite(root_name)
            self.parse_case_xmind(js_dict[0]['rootTopic'], case_dict)
            return req_dict, case_dict

    def req_check_suite_or_case(self, in_data, father):
        if "children" not in in_data.keys() or in_data['children'] == {}:
            if father == '需求分析':
                return "suite"
            else:
                return "case"
        else:
            return "suite"

    def case_check_suite_or_case(self, in_data, father):
        #if "children" not in in_data.keys() or in_data['children'] == {}:
        #    if father == "需求分析" or father == "用例":
        #        return "suite"
        #    return "case"
        #else:
        #    return "suite"
        return "suite"

    def parse_req_xmind(self, in_data, out_dict, start = 0, pre_dict = {}, count = 0, req_spec = '', req = '', save_custom = [], repeat_argv = '', father = '', tf_name = ''):
        if "title" in in_data.keys():
            if in_data['title'] == "需求分析":
                father = in_data['title']
                start = 1
            elif in_data['title'] != "需求分析":
                sc = self.req_check_suite_or_case(in_data, father)
                if sc == "case":
                    case = self.create_base_case(in_data, pre_dict, count, req_spec, req)
                    out_dict['cases'].append(case)
                    return 1
                elif sc == "suite":
                    father = in_data['title']
                    #if len(in_data['title']) >= 100:
                    #    print('Warning :' + in_data['title'])
                    repeat_argv = repeat_argv + in_data['title'] + "~"
                    suite_detail = ""
                    if "notes" in in_data.keys():
                        suite_detail = in_data["notes"]["plain"]["content"]
                    new_tf_name = self._get_tf_name(suite_detail)
                    if new_tf_name != '':
                        tf_name = new_tf_name
                    suite = self.create_suite(in_data['title'], suite_detail)
                    out_dict['suites'].append(suite)
                    out_dict = suite
        if "notes" in in_data.keys():
            #测试集的摘要
            suite_detail = in_data["notes"]["plain"]["content"]
        if "children" in in_data.keys():
            if "attached" in in_data['children']:
                #递归，遍历嵌套的节点
                for count in range(len(in_data['children']['attached'])):
                    attach = in_data['children']['attached'][count]
                    if isinstance(attach, dict):
                        if not self.have_req(attach) and start == 0:
                            continue
                        else:
                            self.parse_req_xmind(attach, out_dict, start, pre_dict, count, req_spec, req, save_custom, repeat_argv, father, tf_name)

    def parse_case_xmind(self, in_data, out_dict, start = 0, pre_dict = {}, count = 0, req_spec = '', req = '', save_custom = [], repeat_argv = '', father = '', tf_name = ''):
        if "title" in in_data.keys():
            if in_data['title'] == "用例":
                father = in_data['title']
                start = 1
            elif in_data['title'] != "用例":
                sc = self.case_check_suite_or_case(in_data, father)
                if sc == "case":
                    case = self.create_base_case(in_data, pre_dict, count, req_spec, req)
                    out_dict['cases'].append(case)
                    return 1
                elif sc == "suite":
                    father = in_data['title']
                    #if len(in_data['title']) >= 100:
                    #    print('Warning :' + in_data['title'])
                    repeat_argv = repeat_argv + in_data['title'] + "~"
                    suite_detail = ""
                    if "notes" in in_data.keys():
                        suite_detail = in_data["notes"]["plain"]["content"]
                    new_tf_name = self._get_tf_name(suite_detail)
                    if new_tf_name != '':
                        tf_name = new_tf_name
                    suite = self.create_suite(in_data['title'], suite_detail)
                    out_dict['suites'].append(suite)
                    out_dict = suite
        if "notes" in in_data.keys():
            #测试集的摘要
            suite_detail = in_data["notes"]["plain"]["content"]
        if "children" in in_data.keys():
            if "attached" in in_data['children']:
                #递归，遍历嵌套的节点
                for count in range(len(in_data['children']['attached'])):
                    attach = in_data['children']['attached'][count]
                    if isinstance(attach, dict):
                        if not self.have_case(attach) and start == 0:
                            continue
                        else:
                            self.parse_case_xmind(attach, out_dict, start, pre_dict, count, req_spec, req, save_custom, repeat_argv, father, tf_name)

    def create_base_case(self, in_data, pre_dict, num, req_spec, req):
        case = {
                'title':'',
                'summary':'',
                }
        if "title" in in_data.keys():
            case['title'] = in_data['title'].strip(" .,").replace('','')
        if "notes" in in_data.keys():
            case['summary'] = self.get_summery(in_data['notes'])
        return case

    def get_module_branch_dict(self, xmind_file, branch_name):
        if self.type == "case_req":
            pp = preprocess.PreProcess()
            js_dict = pp.start(xmind_file)
            root_name = self.get_root(js_dict)

            root_dict = self.create_suite(root_name)
            if branch_name == '':
                self.branch_start = 1
            self.get_branch_dict(js_dict[0]['rootTopic'], root_dict, branch_name)
            #self.get_branch_dict(js_dict[0]['rootTopic'], root_dict, 'module')

            return root_dict

if __name__ == "__main__":
    js_file = "content.json"
    with open(js_file) as jf:
        js_dict = json.load(jf)
    xd = XmindToDict()
    root_dict = {}
    root_name = xd.get_root(js_dict)
    root = xd.create_suite(root_name)
    xd.get_req_dict(js_dict[0]['rootTopic'],root)
    print(root['suites'][0])
