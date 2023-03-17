# WeChat-Bot

## 如何使用
0. 安装python 例如：python 3.8.x
1. 安装微信 3.7.0.30
2. 安装依赖
```python
# 升级pip
pip install -U pip
# 安装必要的依赖
pip install -r requirements.txt
```
3. 在 `proxies` 中填入你自己的代理，如果需要的话
4. 在 `api_key` 中填入你的key


## 更新
- **2023.3.17** 配置了chatgpt
  1. 本来是打算用itcaht的，封麻了，只能再找轮子了
  2. chatgpt支持上下文统计 ，还没弄，再了解一下
    ```python
    res = await api.sendMessage('What were we talking about?', {
        parentMessageId: res.id
    })
    ``` 

  
## 参考
- https://github.com/openai/openai-cookbook
- https://github.com/PlexPt/awesome-chatgpt-prompts-zh
- 待更新