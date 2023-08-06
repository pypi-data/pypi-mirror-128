import requests
import json
"""
GET DLELETE
token	是	query	无	用户令牌，可直接加到请求地址后，如：http://www.pushplus.plus/send/{token}?content=XXX
title	否	query	无	消息标题
content	是	query	无	具体消息内容，根据不同template支持不同格式
template	否	query	html	发送消息模板
channel	否	query	wechat	发送渠道
webhook	否	query	无	webhook编码，仅在channel使用webhook渠道和CP渠道时需要填写
callbackUrl	否	query	无	回调地址，异步回调发送结果
timestamp	否	query	无	时间戳，毫秒。如小于当前时间，消息将无法发送
http://www.pushplus.plus/send?token=XXX&title=XXX&content=XXX&template=html
"""
"""
HTTP POST和PUT请求
http://www.pushplus.plus/send
Content-Type: application/json

参数名称

是否必须

参数类型

默认值

描述

token	是	body	无	用户令牌
title	否	body	无	消息标题
content	是	body	无	具体消息内容，根据不同template支持不同格式
template	否	body	html	发送消息模板
channel	否	body	wechat	发送渠道
webhook	否	body	无	webhook编码，仅在channel使用webhook渠道和CP渠道时需要填写
callbackUrl	否	body	无	回调地址，异步回调发送结果
timestamp	否	body	无	时间戳，毫秒。如小于当前时间，消息将无法发送
"""
"""
模板枚举
template消息模板枚举
模板名称

描述

html	支持html文本。为空默认使用html模板
txt	纯文本内容,不转义html内容,换行使用\n
json	可视化展示json格式内容
markdown	内容基于markdown格式展示
cloudMonitor	阿里云监控报警定制模板
发送渠道枚举
channel发送渠道枚举
发送渠道

描述

wechat	微信公众号,默认发送渠道
webhook	第三方webhook服务；企业微信机器人、钉钉机器人、飞书机器人
cp	企业微信应用
mail	邮件
sms	短信，未开放使用"""
class push():
    def __init__(self,token,title='push推送',content='push推送',template='html'):
        self.token = token
        self.title = title
        self.content = content
        self.template = template
    def get_deleate(self):
        try:
            zhi=requests.get('http://www.pushplus.plus/send?token={}&title={}&content={}&template={}'.format(self.token,self.title,self.content,self.template))
            response=json.loads(zhi.text)
            code=response['code']
            if code =='200':
                print('请求成功')
            else:
                print(response['msg'])


        except:
            print('请求失败，检查token是否正确')

    def post_put(self):
        try:
            data={'token':self.token,'title':self.title,'content':self.content,'template':self.template}
            zhi=requests.post('http://www.pushplus.plus/send',data=data)
            response = json.loads(zhi.text)
            code = response['code']
            if code == '200':
                print('请求成功')
            else:
                print(response['msg'])
        except:
            print('请求失败，检查token是否正确')

if __name__=='__main__':
    qingqiu=push('',title='成功',content='成功')
    qingqiu.post_put()
