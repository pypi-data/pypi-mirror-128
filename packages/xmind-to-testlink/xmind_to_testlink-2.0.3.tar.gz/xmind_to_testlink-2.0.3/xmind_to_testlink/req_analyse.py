from __future__ import unicode_literals
import zipfile
import os
import time
import re
import copy
import sys
import codecs
import json
import argparse
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import xmind_to_dict
import req_rexmind as rr

register_list = []
reg_conf_list = []
other_conf_list = []

def get_dpath(in_dict, pre_path = ''):
    path_list = []
    for k in in_dict:
        l1_path = os.path.join(pre_path, k)
        if isinstance(in_dict[k], list):
            for n,v in enumerate(in_dict[k]):
                l2_path = os.path.join(l1_path, str(n))
                path_list.append(l2_path.strip("/"))
                if k != "cases":
                    path_list.extend(get_dpath(v, l2_path))
    return path_list

def get_suite_case_path_list(path_list):
    suite_path_list = []
    case_path_list = []
    for path in path_list:
        if path.find('cases') >= 0:
            case_path_list.append(path)
        else:
            suite_path_list.append(path)
    return suite_path_list,case_path_list

def get_delem(in_dict, dpath, key = ''):
    path = dpath.strip('/').split('/')
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
        else:
            msg += "[\'"  + i + "\']"
    if key != '':
        msg += "[\'"  + key + "\']"
    return eval("in_dict" + msg)

def get_father_delem(in_dict, dpath, key = ''):
    path = dpath.strip('/').split('/')
    path = dpath.strip('/').split('/')[:-2]
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
        else:
            msg += "[\'"  + i + "\']"
    if key != '':
        msg += "[\'"  + key + "\']"
    return eval("in_dict" + msg)

def transfer_path(in_dict, dpath):
    path = dpath.strip('/').split('/')
    cnpath = ''
    msg = ''
    for i in path:
        if i.isdigit():
            msg += "["  + i + "]"
            cnpath += eval("in_dict" + msg)['title'] + "/"
        else:
            msg += "[\'"  + i + "\']"
    return cnpath.strip("/").replace("：", ':')
    #return '/'.join(cnpath.split('/')[1:])

def check_reg(reg_conf):
    #print("reg_conf: " + reg_conf)
    global register_list
    global reg_conf_list
    global other_conf_list
    find = 0

    for reg in register_list:
        if reg.endswith(reg_conf):
            find = 1
            reg_conf_list.append(reg)
            register_list.remove(reg)
            break
    if not find:
        for creg in reg_conf_list:
            if creg.endswith(reg_conf):
                find = 1
                break
    if not find:
        other_conf_list.append(reg_conf)

def show_path_list(path_list, in_dict):
    for i in path_list:
        print(i)
        print(transfer_path(in_dict, i))

def find_req(root_dict, in_path):
    tmp = in_path.split('/')
    for i in range(int(len(tmp)/2)):
        tmp_path = '/'.join(tmp[:2*(i+1)])
        delem = get_delem(root_dict, tmp_path)
        msg = ''
        if tmp_path.find('cases') >= 0:
            msg = delem['summary']
        else:
            msg = delem['detail']
        if msg != '':
            for j in msg.split('\n'):
                if j.startswith('[[') and j.endswith(']]'):
                    delem = fix_title(delem)
                    return delem, i
    return None, None

def fix_title(elem):
    new_elem = copy.deepcopy(elem)
    for index in range(len(elem['suites'])):
        i = elem['suites'][index]
        if i['title'] == '用例名' and len(i['suites']) != 0:
            new_elem['title'] = i['suites'][0]['title']
            del new_elem['suites'][index]
            break
    return new_elem

def get_flist(fdir):
    flist = []
    for i in os.listdir(fdir):
        path = os.path.join(fdir, i)
        if os.path.isdir(path):
            flist.extend(get_flist(path))
        elif path.find('.xmind') >= 0:
            flist.append(path)
    return flist

    



def check_xmind(xmind_file = '', is_module = 0):
    parser = argparse.ArgumentParser(description = "") 
    parser.add_argument('-f', '--file', dest='file', metavar='File', nargs="+", \
            help='file')
    parser.add_argument('-d', '--dir', dest='dir', metavar='Dir', nargs="+", \
            help='file directory')
    parser.add_argument('-b', '--branch_name', dest='branch', metavar='Branch', \
            help='branch name')
    parser.add_argument('-n', '--node_index', dest='node', metavar='Node', nargs="+", \
            help='node index')
    args = parser.parse_args()
    #print(args)
    branch_name = '模块测试'
    node_index = 3
    if args.branch != None:
        branch_name = args.branch
    if args.node != None:
        node_index = int(args.node[0])
    test_file_list = []
    if args.dir != None:
        for xmind_dir in args.dir:
            test_file_list.extend(get_flist(xmind_dir))
    elif args.file != None:
        test_file_list = args.file
    else:
        sys.exit()

    print(test_file_list)
    for xmind_file in test_file_list:
        xmind_type = "case_req"
        print(xmind_file)
        xmind_name = os.path.basename(xmind_file)

        xd = xmind_to_dict.XmindToDict(xmind_type)
        root_dict = xd.get_module_branch_dict(xmind_file, branch_name)
        path_list = get_dpath(root_dict)
        #print(path_list)
        suite_path_list, case_path_list = get_suite_case_path_list(path_list)
        path_req_list = []
        path_case_list = []
        cn_path_req_dict = {}
        for i in suite_path_list:
            cn_path = transfer_path(root_dict, i)
            if cn_path.find('/需求分析/') >= 0:
                path_req_list.append(i)
                cn_path_req_dict[cn_path] = i
            elif cn_path.find('/用例/') >= 0:
                path_case_list.append(i)
            elif cn_path.find('/功能特性/') >= 0:
                path_req_list.append(i)
                cn_path_req_dict[cn_path] = i

        #show_path_list(path_req_list, root_dict)
        #show_path_list(path_case_list, root_dict)
        print(cn_path_req_dict)
        case_delem_list = []
        for i in path_case_list:
            delem, index = find_req(root_dict, i)
            #if delem and delem not in case_delem_list:
            if delem :
                tmp_find = 0
                for tmp_delem in case_delem_list:
                    if tmp_delem['data'] == delem:
                        tmp_find = 1
                if not tmp_find:
                    case_delem_list.append({'data':delem,
                                        'dpath':i,    
                                        'cn_path':transfer_path(root_dict, i),
                                        'index':index,
                                        })


        for delem in case_delem_list:
            if delem != None:
                if 'summary' in delem['data']:
                    msg = delem['data']['summary']
                elif 'detail' in delem['data']:
                    msg = delem['data']['detail']

                for j in msg.split('\n'):
                    if j.startswith('[[') and j.endswith(']]'):
                        req = j[2:-2]
                        #req = req.replace(' ', '').replace(chr(0xa0), '').replace(chr(0x30), '')
                        req = req.replace(' ', '').replace(chr(0xa0), '')
                        print(req)
                        for k,v in cn_path_req_dict.items():
                            #print(req, k, k.endswith(req))
                            if k.endswith(req):
                                print('path: ' + k)
                                req_elem = get_delem(root_dict, v)
                                if len(req_elem['suites']) == 0:
                                    req_elem['suites'].append({
                                        'title':'测试用例',
                                        'detail':'',
                                        'suites':[],
                                        'cases':[]
                                        })
                                tmp_path = delem['cn_path'].split('/')[node_index:delem['index']]
                                print(tmp_path)
                                node_path = '/'.join(tmp_path)
                                case_elem = check_req_elem(req_elem['suites'][0], tmp_path)
                                case_elem['suites'].append(copy.deepcopy(delem['data']))
                                #case_elem['suites'][-1]['title'] =  \
                                #        '/'.join(delem['cn_path'].split('/')[3:delem['index']])
        with open('save_dict.py','w') as fd:
            fd.write('dict2 = ' + str(root_dict))
        #print(root_dict)
        rr.md_to_xmind(xmind_name, root_dict)


def check_req_elem(elem, tmp_path):
    for tmp in tmp_path:
        have_tmp = 0 
        index = 10000
        for i in range(len(elem['suites'])):
            suite = elem['suites'][i]
            if suite['title'] == tmp:
                have_tmp = 1
                index = i
                break
        if not have_tmp:
            elem['suites'].append({
                'title':tmp,
                'detail':'',
                'suites':[],
                'cases':[]
                })
            elem = elem['suites'][-1]
        else:
            elem = elem['suites'][index]
    return elem

    



if __name__ == "__main__":
    check_xmind()
