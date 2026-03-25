"""
wxauto 兼容层 - 将 wxautox4 的 API 适配为旧版 wxauto 的接口
"""

import time
import logging
import queue
from typing import List, Dict, Any, Optional

# 导入 wxautox4
try:
    from wxautox import WeChat as WeChatX4
except ImportError:
    try:
        from wxautox4 import WeChat as WeChatX4
    except ImportError:
        raise ImportError("无法导入 wxautox 或 wxautox4，请确保已安装付费版 wxautox4")

logger = logging.getLogger('main')


class WeChat:
    """模拟旧版 wxauto 的 WeChat 类"""
    
    def __init__(self):
        """初始化微信连接"""
        try:
            self._wx = WeChatX4()
            logger.info("wxautox4 初始化成功")
        except Exception as e:
            logger.error(f"wxautox4 初始化失败: {e}")
            raise
        
        # 消息队列（用于模拟 GetListenMessage）
        self._message_queue = queue.Queue()
        
        # 模拟 A_MyIcon 对象
        class MyIcon:
            def __init__(self, parent):
                self._parent = parent
            
            @property
            def Name(self):
                try:
                    if hasattr(self._parent._wx, 'GetMyInfo'):
                        info = self._parent._wx.GetMyInfo()
                        return info.get('name', 'KouriChat')
                    else:
                        return "KouriChat"
                except Exception:
                    return "KouriChat"
        
        self.A_MyIcon = MyIcon(self)
        
        # 模拟 ChatBox 属性
        class ChatBoxWrapper:
            def __init__(self, parent):
                self.parent = parent
            
            def ButtonControl(self, Name=None):
                class Button:
                    def Exists(self, timeout=1):
                        return True
                    def Click(self):
                        logger.info(f"点击按钮: {Name}")
                        return True
                return Button()
        
        self.ChatBox = ChatBoxWrapper(self)
    
    def GetSessionList(self) -> List:
        """获取会话列表"""
        try:
            if hasattr(self._wx, 'GetSession'):
                sessions = self._wx.GetSession()
                if sessions:
                    return [session.info.get('name', '') for session in sessions]
                return []
            else:
                logger.warning("GetSessionList 不可用，返回模拟数据")
                return ["微信"]
        except Exception as e:
            logger.error(f"GetSessionList 失败: {e}")
            return []
    
    def ChatWith(self, who: str) -> bool:
        """切换到指定聊天窗口"""
        try:
            if hasattr(self._wx, 'ChatWith'):
                return self._wx.ChatWith(who)
            else:
                logger.warning(f"ChatWith 不可用，跳过: {who}")
                return False
        except Exception as e:
            logger.error(f"ChatWith 失败 ({who}): {e}")
            return False
    
    def AddListenChat(self, nickname: str, savepic: bool = True, savevoice: bool = True):
        """添加聊天监听"""
        try:
            if hasattr(self._wx, 'AddListenChat'):
                # 创建包装回调，将消息放入队列
                def wrapped_callback(msg, chat):
                    """将 wxautox4 的消息转换为旧版格式并放入队列"""
                    try:
                        logger.info(f"【回调触发】收到消息: 来自 {nickname}")
                        
                        # 获取消息内容
                        msg_content = getattr(msg, 'content', '')
                        logger.info(f"消息内容: {msg_content}")
                        
                        # 创建类似旧版的消息对象
                        class SimulatedMsg:
                            def __init__(self, msg_obj, chat_name):
                                self._msg = msg_obj
                                self.type = getattr(msg_obj, 'type', 'friend')
                                self.content = getattr(msg_obj, 'content', '')
                                self.sender = getattr(msg_obj, 'sender', chat_name)
                                self.id = getattr(msg_obj, 'id', str(time.time()))
                            
                            def __str__(self):
                                return str(self.content)
                        
                        class SimulatedChat:
                            def __init__(self, chat_obj, name):
                                self._chat = chat_obj
                                self.who = name
                            
                            def __str__(self):
                                return self.who
                        
                        simulated_msg = SimulatedMsg(msg, nickname)
                        simulated_chat = SimulatedChat(chat, nickname)
                        
                        # 放入消息队列
                        self._message_queue.put((simulated_chat, [simulated_msg]))
                        logger.info(f"消息已放入队列，当前队列大小: {self._message_queue.qsize()}")
                        
                    except Exception as e:
                        logger.error(f"包装回调处理失败: {e}")
                
                # 调用 wxautox4 的 AddListenChat
                result = self._wx.AddListenChat(nickname, wrapped_callback)
                logger.info(f"AddListenChat 返回: {result}")
                return result
            else:
                logger.warning(f"AddListenChat 不可用，跳过: {nickname}")
                return None
                
        except Exception as e:
            logger.error(f"AddListenChat 失败 ({nickname}): {e}")
            return None
    
    def GetListenMessage(self) -> Dict:
        """获取监听到的消息（从队列中获取）"""
        # logger.info(f"GetListenMessage 被调用 - 当前队列大小: {self._message_queue.qsize()}")
        try:
            messages = {}
            # 从队列中取出所有消息
            while not self._message_queue.empty():
                try:
                    chat, msgs = self._message_queue.get_nowait()
                    messages[chat] = msgs
                    logger.info(f"从队列取出消息: {chat.who}, 共 {len(msgs)} 条")
                except queue.Empty:
                    break
            return messages
        except Exception as e:
            logger.error(f"GetListenMessage 失败: {e}")
            return {}
    
    def SendMsg(self, msg: str, who: str = None):
        """发送消息"""
        try:
            if not who:
                logger.error("发送消息需要指定 who 参数")
                return False
            
            logger.info(f"准备发送消息到 {who}: {msg}")
            
            # 先切换到指定聊天窗口
            if not self.ChatWith(who):
                logger.error(f"切换到聊天窗口失败: {who}")
                return False
            
            # 使用 GetSubWindow 获取聊天对象
            if hasattr(self._wx, 'GetSubWindow'):
                chat = self._wx.GetSubWindow(nickname=who)
                if chat:
                    # Chat 对象有 SendMsg 方法
                    result = chat.SendMsg(msg)
                    logger.info(f"发送结果: {result}")
                    return result
                else:
                    logger.error(f"获取聊天窗口对象失败: {who}")
                    return False
            else:
                logger.warning("GetSubWindow 不可用")
                return False
                
        except Exception as e:
            logger.error(f"SendMsg 失败: {e}")
            return False
    
    def GetLastMessage(self) -> Optional[str]:
        """获取最后一条消息"""
        try:
            if hasattr(self._wx, 'get_last_message'):
                return self._wx.get_last_message()
            else:
                return None
        except Exception:
            return None
    
    def GetHwnd(self) -> Optional[int]:
        """获取窗口句柄"""
        try:
            if hasattr(self._wx, 'GetHwnd'):
                return self._wx.GetHwnd()
            elif hasattr(self._wx, 'hwnd'):
                return self._wx.hwnd
            else:
                return None
        except Exception:
            return None
    
    def KeepRunning(self):
        """保持程序运行"""
        try:
            if hasattr(self._wx, 'KeepRunning'):
                return self._wx.KeepRunning()
        except Exception as e:
            logger.error(f"KeepRunning 失败：{e}")
    
    def SendFiles(self, filepath: str, friend: str = None, who: str = None):
        """发送文件/表情包到聊天窗口
        
        Args:
            filepath: 文件路径
            friend: 聊天对象名称（新版参数）
            who: 聊天对象名称（旧版兼容参数）
        """
        try:
            # 兼容两种参数名
            target = friend or who
            if not target:
                logger.error("SendFiles 需要指定 friend 或 who 参数")
                return False
            
            logger.info(f"准备发送文件：{filepath} 到 {target}")
            
            # 先切换到指定聊天窗口
            if not self.ChatWith(target):
                logger.error(f"切换到聊天窗口失败：{target}")
                return False
            
            # 使用 GetSubWindow 获取聊天对象
            if hasattr(self._wx, 'GetSubWindow'):
                chat = self._wx.GetSubWindow(nickname=target)
                if chat:
                    # 尝试使用 SendImage 或 SendFiles 方法
                    if hasattr(chat, 'SendImage'):
                        result = chat.SendImage(filepath)
                        logger.info(f"SendImage 发送结果：{result}")
                        return result
                    elif hasattr(chat, 'SendFiles'):
                        result = chat.SendFiles(filepath)
                        logger.info(f"SendFiles 发送结果：{result}")
                        return result
                    else:
                        # 尝试直接调用 SendMsg（某些版本可能支持）
                        logger.warning("聊天对象没有 SendImage 或 SendFiles 方法")
                        return False
                else:
                    logger.error(f"获取聊天窗口对象失败：{target}")
                    return False
            else:
                logger.warning("GetSubWindow 不可用")
                return False
                
        except Exception as e:
            logger.error(f"SendFiles 失败：{e}")
            return False
    
    def _show(self):
        """显示窗口"""
        try:
            if hasattr(self._wx, '_show'):
                return self._wx._show()
            elif hasattr(self._wx, 'show'):
                return self._wx.show()
        except Exception as e:
            logger.error(f"_show 失败: {e}")


class ChatWnd:
    """模拟旧版 wxauto.elements.ChatWnd 类"""
    
    def __init__(self, who=None, language='zh_CN'):
        self.who = who
        self.language = language
        self._wx = WeChat()
    
    def _show(self):
        return self._wx._show()
    
    @property
    def UiaAPI(self):
        class UiaAPIWrapper:
            def __init__(self, parent):
                self.parent = parent
            
            def ButtonControl(self, Name=None):
                class Button:
                    def Exists(self, timeout=1):
                        return True
                    def Click(self):
                        logger.info(f"点击按钮: {Name}")
                        return True
                return Button()
        
        return UiaAPIWrapper(self)


__all__ = ['WeChat', 'ChatWnd']