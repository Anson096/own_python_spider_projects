# !/usr/bin/python
# -*- coding:utf-8 -*-
#  __Author:Anson__

import urllib.request
import urllib.parse
import urllib.response
import json

word_notebook = {}
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


def find_trans(trans):
    form_data = {'i': trans,
                 'from': 'AUTO',
                 'to': 'AUTO',
                 'smartresult': 'dict',
                 'client': 'fanyideskweb',
                 'salt': '1530710031702',
                 'sign': 'a77106712e1552d97538edad391d8a90',
                 'doctype': 'json',
                 'version': '2.1',
                 'keyfrom': 'fanyi.web',
                 'action': 'FY_BY_REALTIME',
                 'typoResult': 'false'
                 }
    data = urllib.parse.urlencode(form_data).encode('utf-8')
    request = urllib.request.Request(url, data, headers=header, method='POST')
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    result = json.loads(html)['translateResult'][0][0]['tgt']
    return result


def add_to_dict(word, tran):
    word_notebook[word] = tran
    print('已将%s加入单词本，翻译为%s' % (word, tran))


def find_in_dict(key):
    try:
        expected_trans = word_notebook[key]
        return expected_trans
    except:
        return 0


while True:
    print('=' * 20)
    want = input('按1查询知识并加入单词本，按2查询单词本，按3删除单词，按4退出 ')
    if want == '1':
        tran_expected = input('想翻译啥？')
        translation = find_trans(tran_expected)
        add_to_dict(tran_expected, translation)
    elif want == '2':
        find_expected = input('想查找啥？')
        find = find_in_dict(find_expected)
        if find != 0:
            print(find)
        else:
            print('目前单词本中无此词')
            translation = find_trans(find_expected)
            add_to_dict(find_expected, translation)
    elif want == '3':
        keys = word_notebook.keys()
        print(keys)
        delete = input('你想删哪个？')
        try:
            word_notebook.pop(delete)
            print('已删除%s' % delete)
        except:
            print('无此词或输入错误')
    elif want == '4':
        print('退出')
        break
    else:
        print('输入错误')
