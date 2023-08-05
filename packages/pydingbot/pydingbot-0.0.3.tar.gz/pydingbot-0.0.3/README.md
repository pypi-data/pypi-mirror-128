# pydingbot
[![Build Status](https://app.travis-ci.com/Clarmy/pydingbot.svg?branch=main)](https://app.travis-ci.com/github/Clarmy/pydingbot)
[![PyPI version](https://badge.fury.io/py/pydingbot.svg)](https://badge.fury.io/py/pydingbot)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Clarmy/pydingbot/issues)

pydingbot 是一个让钉钉机器人更好用的包。

## 安装
你可以用 `pip` 来安装pydingbot
```shell
$ pip install pydingbot
```

## 使用

在使用pydingbot之前，首先你需要在钉钉群里添加你的自定义机器人，安全设置选择**加签**，然后点开“机器人设置”找到 **webhook** 和 **secret**（秘钥），这些是使用机器人所必须的信息，webhook和secret的来源如图所示：   

![config](docs/static/config.png)   

### 简单示例

```python
from pydingbot import inform

WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864e90502b48603ecbcd7646701bd66cc590f495bac1b7c5049e171e'
SECRET = 'SEC474937571de1506cdd724af0d5866f4fa2788968032a2d6d982da988bea4e5de'

inform(webhook=WEBHOOK, secret=SECRET, title='My Title', text='My Text')
```
如果你的配置正确，那么消息应该就已经发送到你的钉钉群里了。   

### 使用@功能

@指定人员需要向`at_mobiles`参数传入指定@人员的手机号列表，例如：

```python
inform(webhook=webhook, secret=secret, title='My Title', text='My Text', at_mobiles=['15811112009', '15822222009'])
```

@所有人需要向`at_all`参数传入`True`，例如：

```python
inform(webhook=webhook, secret=secret, title='My Title', text='My Text', at_all=True)
```

还可以同时使用@指定人和@所有人的功能，例如：

```python
inform(webhook=webhook, secret=secret, title='My Title', text='My Text', at_mobiles=['15811112009', '15822222009'], at_all=True)
```