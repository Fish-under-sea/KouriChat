import logging
import time
import win32gui
import pygame
from wxautox4 import WeChat        # ✅ 修改：从 wxautox4 导入
from wxautox4.msgs import FriendMessage  # 如果需要消息处理
# ❌ 删除：from wxauto.elements import ChatWnd
import uiautomation

logger = logging.getLogger('main')

# --- 配置参数 ---
CALL_WINDOW_CLASSNAME = 'AudioWnd'
CALL_WINDOW_NAME = '微信'
CALL_BUTTON_NAME = '语音聊天'
HANG_UP_BUTTON_NAME = '挂断'
HANG_UP_BUTTON_LABEL = '挂断'
REFUSE_MSG = '对方已拒绝'
CALL_TIME_OUT = 15


def CallforWho(wx: WeChat, who: str) -> tuple[int|None, bool]:
    """
    对指定对象发起语音通话请求。

    Args:
        wx: 微信应用实例。
        who: 通话对象。

    Returns:
        若拨号成功，返回元组 (句柄号, True)。
        否则返回 (None, False)。
    """
    logger.info("尝试发起语音通话")
    try:
        # wxautox4 使用 ChatWith 打开聊天窗口，然后用 GetSubWindow 获取 Chat 对象
        wx.ChatWith(who)
        
        # 获取子窗口（Chat 对象）
        chat = wx.GetSubWindow(nickname=who)
        
        if chat:
            # 使用 uiautomation 直接操作按钮（wxautox4 内部使用 uiautomation）
            # 或者通过 chat 对象的方法来操作
            
            # 方法1：使用 uiautomation 直接查找按钮
            # 需要找到聊天窗口的句柄
            hwnd = win32gui.FindWindow(None, who)  # 查找聊天窗口
            
            if hwnd:
                chat_window = uiautomation.ControlFromHandle(hwnd)
                voice_call_button = chat_window.ButtonControl(Name=CALL_BUTTON_NAME)
                if voice_call_button.Exists(1):
                    voice_call_button.Click()
                    logger.info("已发起通话")
                    time.sleep(0.5)
                    call_hWnd = win32gui.FindWindow(CALL_WINDOW_CLASSNAME, CALL_WINDOW_NAME)
                    return call_hWnd, True
                else:
                    logger.error("发起通话时发生错误：找不到通话按钮")
                    return None, False
            else:
                logger.error("找不到聊天窗口")
                return None, False
        else:
            logger.error("无法获取聊天窗口对象")
            return None, False

    except Exception as e:
        logger.error(f"发起通话时发生错误: {e}")
        return None, False


def CancelCall(hWnd: int) -> bool:
    """
    取消/终止语音通话。

    Args:
        hWnd: 通话窗口的句柄号。

    Returns:
        若取消/终止成功，返回 True。
        否则返回 False。
    """
    logger.info("尝试挂断语音通话")

    if not hWnd:
        logger.error("找不到通话句柄")
        return False

    try:
        call_window = uiautomation.ControlFromHandle(hWnd)
        if not call_window:
            logger.error("无法获取通话窗口控件")
            return False
            
        hang_up_button = call_window.ButtonControl(Name=HANG_UP_BUTTON_NAME)
        if hang_up_button.Exists(1):
            # 窗口置顶操作
            win32gui.ShowWindow(hWnd, 1)
            win32gui.SetWindowPos(hWnd, -1, 0, 0, 0, 0, 3)
            win32gui.SetWindowPos(hWnd, -2, 0, 0, 0, 0, 3)
            call_window.SwitchToThisWindow()
            hang_up_button.Click()
            logger.info("语音通话已挂断")
            return True
        else:
            logger.error("挂断通话时发生错误：找不到挂断按钮")
            return False

    except Exception as e:
        logger.error(f"挂断通话时发生错误: {e}")
        return False


def PlayVoice(audio_file_path: str, device=None) -> bool:
    """
    播放指定的音频文件到指定的音频输出设备。
    
    Args:
        audio_file_path: 要播放的音频文件路径。
        device: (可选)音频输出设备的名称。
                            默认为 None，此时会使用系统默认输出设备。
    
    Returns:
        若完整播放，返回 True。
        否则返回 False。
    """
    logger.info(f"尝试播放音频文件: '{audio_file_path}'")

    if device:
        logger.info(f"目标输出设备: '{device}'")
    else:
        logger.info("目标输出设备: 系统默认")

    try:
        pygame.mixer.quit()
        pygame.mixer.init(devicename=device)
        pygame.mixer.music.load(audio_file_path)
        time.sleep(2)
        pygame.mixer.music.play()
        logger.info("开始播放音频...")

        # 等待音频播放完毕
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        logger.info("音频播放完毕。")
        return True

    except pygame.error as e:
        logger.error(f"Pygame 错误:{e}")
        return False
    except FileNotFoundError:
        logger.error(f"音频文件未找到:'{audio_file_path}'")
        return False
    except Exception as e:
        logger.error(f"发生未知错误:{e}")
        return False
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()


def Call(wx: WeChat, who: str, audio_file_path: str) -> None:
    """
    尝试向指定对象发起语音通话，接通后会将指定音频文件输入麦克风，并自动挂断。

    Args:
        wx: 微信实例。
        who: 通话对象。
        audio_file_path: 音频文件路径。
    
    Returns:
        None
    """
    call_hwnd, success = CallforWho(wx, who)
    if not success:
        logger.error("发起通话失败")
        return
    
    logger.info(f"等待对方接听 (等待{CALL_TIME_OUT}秒)...")

    start_time = time.time()
    call_status = 0  # 0: 等待中, 1: 已接通, 2: 已拒接

    try:
        # 等待通话窗口出现
        call_window = None
        while time.time() - start_time < CALL_TIME_OUT:
            if call_hwnd:
                call_window = uiautomation.ControlFromHandle(call_hwnd)
                if not call_window:
                    time.sleep(0.5)
                    continue
                    
                hang_up_text = call_window.TextControl(Name=HANG_UP_BUTTON_LABEL)
                refuse_msg = call_window.TextControl(Name=REFUSE_MSG)
                
                if hang_up_text.Exists(0.1, 0.1) and not refuse_msg.Exists(0.1, 0.1):
                    logger.info("通话已接通！")
                    call_status = 1
                    break
                elif refuse_msg.Exists(0.1, 0.1):
                    logger.info("通话被拒接！")
                    call_status = 2
                    break
            time.sleep(0.5)

        # 根据通话状态执行相应操作
        if call_status == 1:
            PlayVoice(audio_file_path=audio_file_path)
            logger.info("语音播放完成，即将挂断...")
            CancelCall(call_hwnd)
        elif call_status == 2:
            logger.info("对方拒绝了通话")
            # TODO: 可以让 bot 回复信息对拒接表示生气
            CancelCall(call_hwnd)
        else:
            logger.info("在超时时间内，对方未接听通话。")
            # TODO: 可以让 bot 回复信息对未接听表示生气
            CancelCall(call_hwnd)

    except Exception as e:
        logger.error(f"处理通话时发生未知错误: {e}")
        if call_hwnd:
            CancelCall(call_hwnd)


# --- 主程序示例 (仅用于测试版) ---
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    logger.info("程序启动")
    
    try:
        wx = WeChat()
        who = ""  # 输入通话对象名称
        if wx and who:
            Call(wx, who, 'test.mp3')
        else:
            logger.error("未能初始化 WeChat 对象或未指定通话对象。")
    except Exception as main_e:
        logger.error(f"主程序执行过程中发生错误: {main_e}", exc_info=True)

    logger.info("程序结束")