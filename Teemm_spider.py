# !/usr/bin/python
# -*- coding:utf-8 -*-
#  __Author:Anson__


import requests
from lxml import etree
import os

input_url_list = ['guowai/']


def main(url_start_list):
    start_url = 'http://m.teemm.com/'
    later_url = 'http://m.teemm.com'
    for index_of_url_start_list in range(len(url_start_list)):
        url_start_list[index_of_url_start_list] = start_url + url_start_list[index_of_url_start_list]

    # 福利页没有东西，所以根据提供的热门tag查找
    def fuli_tag():
        tag_list = []
        new_url = 'http://m.teemm.com/fuli/'
        response = requests.get(new_url)
        response.encoding = 'gb2312'
        html = etree.HTML(response.text)
        tag_find = html.xpath('//div[@class="all"]/a/@href')
        tag_find.pop(0)
        for each in tag_find:
            str(each)
            print(later_url+each)
            tag_list.append(later_url+each)
        print(tag_list)
        return tag_list


    # 给予每一页的url，进入专栏
    def get_pics_path(url_list_input):
        return_path_list = []
        return_name_list = []

        # 给予第一页的url，返回其之后所有页的url
        def find_outer_index(url_list):
            for url in url_list:
                return_outer_index_list = []
                response = requests.get(url)
                response.encoding = 'gb2312'
                html = etree.HTML(response.text)
                index_find = html.xpath('//select[@name="sldd"]/option/@value')
                for index_of_index_find in range(len(index_find)):
                    str(index_find[index_of_index_find])
                    index_find[index_of_index_find] = url + index_find[index_of_index_find]
                    return_outer_index_list.append(index_find[index_of_index_find])
            if not return_outer_index_list:
                return url_list
            return return_outer_index_list

        for each_url in find_outer_index(url_list_input):
            response = requests.get(each_url)
            response.encoding = 'gb2312'
            html = etree.HTML(response.text)
            path = html.xpath('//div[@class="list_btm"]/ul/li/a/@href')
            name = html.xpath('//div[@class="list_btm"]/ul/li/a/span/b/text()')
            for path_index in range(len(path)):
                str(path[path_index])
                path[path_index] = later_url + path[path_index]
                return_path_list.append(path[path_index])
            for each_name in name:
                str(each_name)
                return_name_list.append(each_name)
            path_name_dict = dict(zip(return_name_list,return_path_list))
        print(path_name_dict)
        return path_name_dict

    # 用刚刚获取的图片路径下载图片
    def download_pics(pics_path_dict):
        for each_name in pics_path_dict:

            # 获取专栏的页码
            def find_inner_index(url):
                response = requests.get(url)
                response.encoding = 'gb2312'
                html = etree.HTML(response.text)
                inner_index = html.xpath('//div[@class="content_page"]/ul/li/a/text()')
                # print(inner_index)
                # print(response.text)
                if inner_index:
                    index = str(inner_index[0])
                    index = index.lstrip('共').rstrip('页: ')
                    return int(index)
                else:
                    print('页码获取失败')

            path = pics_path_dict[each_name]
            index_now = find_inner_index(path)
            if index_now:
                if not os.path.exists('./fuli_pics/{}'.format(each_name)):
                    dictionary_path = './fuli_pics/{}'.format(each_name)
                    os.makedirs(dictionary_path)
                    download_local_path = './fuli_pics/{}/%s.png'.format(each_name)
                    print('正在下载%s' % each_name)
                else:
                    download_local_path = './fuli_pics/{}/%s.png'.format(each_name)
                    print('%s的目录已存在' % each_name)

                # 分割网址，把页码处改为%s
                def split_html(html:str):
                    html_split = html.split('/')
                    pic_id = html_split[-1].split('.')[0]
                    page_list = [pic_id,'_%d.html']
                    html_split[-1] = ''.join(page_list)
                    result = '/'.join(html_split)
                    return result

                for page_count in range(0,index_now-1):
                    if page_count == 0:
                        url = path
                    else:
                        url = split_html(path) % (page_count+1)
                    try:
                        response = requests.get(url)
                        response.encoding = 'gb2312'
                        html = etree.HTML(response.text)
                        download_path = html.xpath('//div[@class="content_cont"]/p/img/@src')[0]
                    except:
                        continue
                    if not os.path.exists(download_local_path % (page_count+1)):
                        with open(download_local_path % (page_count+1),'wb') as f:
                            response = requests.get(download_path)
                            f.write(response.content)
            else:
                continue

    return download_pics(get_pics_path(fuli_tag()))


if __name__ == '__main__':
    main(input_url_list)

