# 使用方法
1. **enable_recv_msg()**
   - 首先判断是否已经在接收消息，如果是，则直接返回`True`。
   - 如果回调函数为空，则返回`False`。
   - 如果回调函数不为空，则向服务器发送一个请求，请求开启接收消息的功能。
   - 如果请求成功，则将`_is_receiving_msg`设置为`True`，表示正在接收消息。然后，启动一个新的线程来接收消息，这个线程会不断地从服务器接收消息，直到`_is_receiving_msg`被设置为`False`。
   - ```python
       源码：
         def enable_recv_msg(self, callback: Callable[[WxMsg], None] = None) -> bool:
        """设置接收消息回调"""
        def listening_msg():
            rsp = wcf_pb2.Response()
            self.msg_socket.dial(self.msg_url, block=True)
            while self._is_receiving_msg:
                try:
                    rsp.ParseFromString(self.msg_socket.recv_msg().bytes)
                except Exception as e:
                    pass
                else:
                    callback(self.WxMsg(rsp.wxmsg))
            # 退出前关闭通信通道
            self.msg_socket.close()

        if self._is_receiving_msg:
            return True

        if callback is None:
            return False

        req = wcf_pb2.Request()
        req.func = wcf_pb2.FUNC_ENABLE_RECV_TXT  # FUNC_ENABLE_RECV_TXT
        rsp = self._send_request(req)
        if rsp.status != 0:
            return False

        self._is_receiving_msg = True
        # 阻塞，把控制权交给用户
        # listening_msg()

        # 不阻塞，启动一个新的线程来接收消息
        Thread(target=listening_msg, name="GetMessage", daemon=True).start()

        return True
     ```
2. **cleanup()**
   - 如果 `self._is_running` 为 `False`，则直接返回
   - 否则关闭接收消息的功能，关闭命令套接字
   - 如果存在本地主机，则发送命令 `f"{WCF_ROOT}/wcf.exe stop"`
   - 如果命令执行失败，则记录错误并返回
   - 最后将 `_is_running` 设置为 `False`
   - ```python
         def cleanup(self) -> None:
        """关闭连接，回收资源"""
            if not self._is_running:
                return

            self.disable_recv_msg()
            self.cmd_socket.close()

            if self._local_host:
                cmd = f"{WCF_ROOT}/wcf.exe stop"
                if os.system(cmd) != 0:
                    self.LOG.error("退出失败！")
                    return
            self._is_running = False
     ```