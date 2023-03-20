# WeChat-Bot

## 如何使用
0. 安装python 例如：python 3.8.x
1. 安装微信 3.7.0.30,下载地址[这个](https://github.com/afanzaimoyu/WeChat-Bot/releases/download/wechat/WeChatSetup-3.7.0.30.exe
)                        **记得把自动更新关了！！！！**
2. 安装依赖
```markdown
# 升级pip
pip install -U pip
# 安装必要的依赖
pip install -r requirements.txt
```
3. 配置json文件
   - `enable`配置群组id
   - `key`配置你的key
   - `proxies`配置你的代理，如果需要的话
   - `initial_prompt`配置你的初始化描述
4. 目前 个人聊天自动接入gpt
5. 群组聊天 需要先@下面是命令
    - ? ：查看帮助
    - 直接跟我聊天 
    - `/init`： 重置对话,回归初始人设 
    - `/remove`： 重置对话 
    - `/reserve`：初始人物设定 创建新的人格 
    - `/prompt` ：查看当前人设

* [WeChat-Bot](#wechat-bot)
  * [如何使用](#如何使用)
  * [待实现 or 问题](#待实现-or-问题)
  * [更新](#更新)
  * [发现的一些好玩的东西](#发现的一些好玩的东西)
  * [有任何问题可以提交issue或者添加我的微信和我联系](#有任何问题可以提交issue或者添加我的微信和我联系)
  * [参考](#参考)
<!-- TOC -->
## 待实现 or 问题
- 多个群聊之间会相互干扰(考虑生产者消费者模型，用多线程或多进程实现)
- ~~初始prompt定死了（特定指令切换prompt并重置聊天）~~
- 导出聊天记录（存起来，特定指令导出）
- ~~自己选择开启新的聊天（能查看当前聊天轮数，特定指令开启）~~
- 群组白名单得手动改代码，虽说改完之后能微信上更新
- 图片
- 
## 更新
- **2023.3.21**
  - 新增每天早上七点发送天气信息 
- **2023.3.19**
  - 新增 `gpt_session.py` 将chat的个性化设置分离出来
  - 新增 上下文功能，聊天不再出戏 ，10轮自动总结上文会话，理论上能一直聊
  - 更新功能
    - ? 查看帮助
    - 直接跟我聊天 
    - `/init` 重置对话,回归初始人设 
    - `/remove` 重置对话 
    - `/reserve`+初始人物设定 创建新的人格 
    - `/prompt` 查看当前人设
   - 
- **2023.3.18**
  - 更新`robot.py` 
    - 新增  自动添加好友并发送自定义消息
    - 新增  微信聊天的方式更新配置文件
    -  新增 用chatgpt与好友聊天
    -  新增  用chatgpt与群友聊天
  - 更新 wcfree.py 用法
  - 
- **2023.3.18** 
  - 更新`gpt.py` 将一些参数丢到了json文件中，方便修改
  - 新建了`job_all.py` 创建了定时类型的任务
  -  新建了`config.json` 配置了日志信息，群组权限，gpt参数
  - 新建了`main.py` 程序主入口，定时消息模块，gpt模块
  -  新建了`my_config.py` 读取配置信息
  -  新建了`robot.py` wx机器人模块，待写
  -   新建了`wcfree.md` 阅读大佬wcfree的源码



- **2023.3.17** 配置了chatgpt
  1. 本来是打算用itcaht的，封麻了，只能再找轮子了

  
## 发现的一些好玩的东西
- [cursor编辑器，免费gpt4](https://www.cursor.so)
- [创建自己的gpt小应用](https://open-gpt.app)
- [gpt4免费的api](https://www.steamship.com/)
-  [查询天气的接口](https://zhwnlapi.etouch.cn/Ecalender/weather_mini?city=北京)

## 有任何问题可以提交issue或者添加我的微信和我联系
<img height="100px" src="D:\Wechat_Bot_GPT\微信图片_20230321015626.jpg" width="100px"/>


## 参考
- [openai使用指南](https://github.com/openai/openai-cookbook)
- [ChatGPT 中文调教指南](https://github.com/PlexPt/awesome-chatgpt-prompts-zh)
- [造轮子的大佬-wcfree](https://github.com/lich0821/WeChatFerry)
- [ChatGPT api + python+赛博女友](https://zhuanlan.zhihu.com/p/610731099)
- [群大佬的wxbot-基于itchat](https://github.com/c0rnP1ex/wxbot_w_gpt)
- [ChatGPT最新模型指南——gpt-3.5-turbo](https://zhuanlan.zhihu.com/p/613581212)
- 待更新