# WeChat-Bot

## 如何使用
0. 安装python 例如：python 3.8.x
1. 安装微信 3.7.0.30,下载地址[这个](https://github.com/afanzaimoyu/WeChat-Bot/releases/download/wechat/WeChatSetup-3.7.0.30.exe
)
2. 安装依赖
```python
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


## 更新
- **2023.3.18**
  - 更新`robot.py` 
    - 新增  自动添加好友并发送自定义消息
    - 新增  微信聊天的方式更新配置文件
    -  新增 用chatgpt与好友聊天
    -  新增  用chatgpt与群友聊天
  - 更新 wcfree.py 用法
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
  2. chatgpt支持上下文统计 ，还没弄，再了解一下
    ```python
    res = await api.sendMessage('What were we talking about?', {
        parentMessageId: res.id
    })
    ``` 

  
## 参考
- [openai使用指南](https://github.com/openai/openai-cookbook)
- [ChatGPT 中文调教指南](https://github.com/PlexPt/awesome-chatgpt-prompts-zh)
- [造轮子的大佬-wcfree](https://github.com/lich0821/WeChatFerry)
- [ChatGPT api + python+赛博女友](https://zhuanlan.zhihu.com/p/610731099)
- [群大佬的wxbot-基于itchat](https://github.com/c0rnP1ex/wxbot_w_gpt)
- 待更新