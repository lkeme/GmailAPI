#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- author: Lkeme
- contact: Useri@live.cn
- file: client.py
- time: 2021/2/18 18:39
- desc:
"""
import re
from app import gmail


class Client:

    def __init__(self, recipient):
        self.recipient = recipient

    def search_query(self):
        """
        哔哩哔哩 <verify@service.bilibili.com>
        【哔哩哔哩】账号安全中心-设置邮箱验证
        尊敬的用户 ，您好:
            您正在哔哩哔哩进行换绑邮箱的操作，本次请求的邮件验证码是：155583(为了保证您账号的安全性，请您在5分钟内完成验证).
            为保证账号安全，请勿泄漏此验证码。
            祝在【哔哩哔哩】收获愉快！

            ( ゜- ゜)つロ乾杯~ - bilibili
            （这是一封自动发送的邮件，请不要直接回复）
        :return:
        """
        # 搜索条件
        # at = int(time.time())
        keyword = '哔哩哔哩'
        conditions = {
            'label': 'UNREAD',
            'from': 'verify@service.bilibili.com',
            'subject': '【哔哩哔哩】账号安全中心-绑定邮箱验证',
            'newer_than': '1d',
            'to': self.recipient,
            # 'subject': '【哔哩哔哩】账号安全中心-设置邮箱验证',
            # 'after': str(time.strftime("%Y/%m/%d", time.localtime(at - 86400))),
            # 'before': str(time.strftime("%Y/%m/%d", time.localtime(at + 86400))),
        }
        query = ''
        for key, value in conditions.items():
            query += f'{key}:{value} '
        return f'{query} {keyword} '

    @staticmethod
    def format_time(dd):
        return dd.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_mail(content):
        try:
            return (re.findall(r'(\d{6})', content))[0]
        except Exception as e:
            return None

    @staticmethod
    def crash(thread):
        # 表示已读
        thread.markAsRead()
        # 删除线程
        thread.trash()

    def query_mail(self):
        # unreadThreads = gmail.unread()  # Returns a list of GmailThread objects.
        # print(gmail.summary(unreadThreads, printInfo=False))
        threads = gmail.search(query=self.search_query())
        # printer(threads)
        # 单独过滤出邮件内容
        # msgs = gmail.summary(threads, printInfo=False)
        for thread in threads:
            # print("-" * 20)
            # threads[0].trash()  # Move the entire first thread to the Trash folder.
            msg = thread.messages[0]
            # print(msg.sender)  # 打印发件人
            # print(msg.recipient)  # 打印收件人
            # print(msg.subject)  # 打印标题
            # print(msg.body)  # 打印内容
            # print(msg.timestamp)  # 打印时间
            # print(msg.snippet) # 打印内容
            sms_code = self.parse_mail(msg.snippet)
            if sms_code is not None:
                # 清理掉
                self.crash(thread)
                return {
                    'code': 0,
                    'msg': 'success',
                    'data': {
                        'sender': msg.sender,
                        'recipient': msg.recipient,
                        'subject': msg.subject,
                        'snippet': msg.snippet,
                        'timestamp': self.format_time(msg.timestamp),
                        'sms_code': sms_code,
                    }
                }
        else:
            return {
                'code': 404,
                'msg': 'no_data',
                'data': {}
            }


if __name__ == '__main__':
    content = """
        哔哩哔哩 <verify@service.bilibili.com>
        【哔哩哔哩】账号安全中心-设置邮箱验证
        尊敬的用户 ，您好:
            您正在哔哩哔哩进行换绑邮箱的操作，本次请求的邮件验证码是：15553(为了保证您账号的安全性，请您在5分钟内完成验证).
            为保证账号安全，请勿泄漏此验证码。
            祝在【哔哩哔哩】收获愉快！

            ( ゜- ゜)つロ乾杯~ - bilibili
            （这是一封自动发送的邮件，请不要直接回复）
        :return:
        """
    print(Client().parse_mail(content))
