# -*- coding: utf-8 -*-
"""
descr: 消息机器人，支持企业微信机器人、飞书机器人、钉钉机器人，etc
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: polaris_message_unit_test.py
"""

from polaris_message.massage_push_bot import WechatBot


if __name__ == '__main__':
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
    bot = WechatBot(webhook_url)
    bot.send_text(content="hello1", mentioned_list=["@all"])
    bot.send_text(content="hello2", mentioned_list=["@all"], mentioned_mobile_list=["18774970063"])
    md = "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n>类型:<font color=\"comment\">用户反馈</font>>普通用户反馈:<font color=\"comment\">117例</font>>VIP用户反馈:<font color=\"comment\">15例</font>"
    bot.send_markdown(content=md)
    bot.send_picture(image_path=r"xxxxxx.png")
    articles = [
        {
            "title": "中秋节礼品领取",
            "description": "今年中秋节公司有豪礼相送",
            "url": "www.qq.com",
            "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        }
    ]
    bot.send_text_picture(articles=articles)
    # filepath = r"xxxxxxx\apiautotest-report-2023-05-11 14_57_18.html"
    # bot.send_file(media_id=bot.upload_file(filepath))
