#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import requests
import random
import re


class Craw(object):

    def unzip(self, data):
        try:
            print("正在解压")
            data = gzip.decompress(data)
            print("解压完毕")
        except:
            print("未经压缩，不需要解压")
        return data

    def get_header(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
            "Safari/537.36"]
        user_agent = random.choice(user_agents)
        req_headers = {
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            'User_Agent': user_agent
        }
        return req_headers

    def get_xsrf(self):
        index_url = "https://www.zhihu.com"
        index_page = requests.session().get(index_url, headers=self.get_header())
        html = index_page.text
        pattern = r'name="_xsrf" value="(.*?)"'
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]

    def login(self, account, secret):
        post_url = 'https://www.zhihu.com/signup?next=%2F'
        post_data = {
            '_xsrf': self.get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
        try:
            # 不需要验证码直接登录成功
            login_page = requests.session().post(post_url, post_data, self.get_header())
            login_code = login_page.text
            print(login_page.status_code)
            print(login_code)
        except:
            print("需要验证码")
        requests.session().cookies.save()


if __name__ == '__main__':
    login = Craw()
    login.login('1562360079', 'haonandu155')

