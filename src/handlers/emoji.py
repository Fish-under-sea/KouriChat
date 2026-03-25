"""
表情包处理模块
负责处理表情包相关功能，包括:
- 表情标签识别
- 表情包选择
- 文件管理
- 表情概率控制
- 颜文字集成
"""

import os
import random
import logging
from typing import Optional, List, Tuple
from datetime import datetime
import pyautogui
import time
from wxauto import WeChat
from data.config import config
from .emoji_keywords import emoji_keyword_handler

logger = logging.getLogger('main')

class EmojiHandler:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        # 修改表情包目录路径为 avatar 目录下的 emojis
        self.emoji_dir = os.path.join(root_dir, config.behavior.context.avatar_dir, "emojis")

        # 支持的表情类型 - 从实际表情包目录动态加载
        self.emotion_types = self._load_emotion_types_from_directory()

        # ========== 表情触发概率配置 ==========
        # 表情包概率配置 - 每次回复都发送表情包
        self.emoji_probability = 1.0  # 100% 概率发送表情包

        # 颜文字概率配置 - 大幅提高触发概率
        self.kaomoji_probability = 0.8  # 80% 基础概率触发颜文字
        self.extreme_emotion_probability = 0.95  # 极端情绪时 95% 概率触发颜文字
        
        # 颜文字插入位置配置
        self.kaomoji_positions = ['end', 'start', 'middle']  # 颜文字可以插入的位置
        self.position_weights = [0.6, 0.2, 0.2]  # 各位置权重：结尾 60%，开头 20%，中间 20%

        # 极端情绪关键词（用于检测情绪强度）
        self.extreme_emotion_keywords = {
            'extreme_happy': ['特别开心', '超级高兴', '太开心了', '兴奋', '激动', '乐疯了', '笑死', '哈哈哈', '嘻嘻嘻'],
            'extreme_angry': ['特别生气', '超级愤怒', '气死了', '气炸了', '太生气了', '火冒三丈', '怒火中烧'],
            'extreme_sad': ['特别难过', '太伤心了', '哭死了', '心碎了', '绝望', '崩溃'],
            'extreme_excited': ['太激动了', '超级兴奋', '激动万分', '兴奋不已'],
            'extreme_joy': ['欣喜若狂', '乐翻天', '开心到飞起', '高兴死了'],
            'extreme_anger': ['暴怒', '发火', '火大', '气冲冲'],
        }

        # 颜文字映射表（情感类型 -> 颜文字列表）- 扩展更多颜文字
        self.kaomoji_map = {
            'happy': [
                '(≧∇≦) ﾉ', '(^▽^)', '(*^ω^)', '(o^▽^o)', 'ヽ (✿ﾟ▽ﾟ) ノ',
                '(◕‿◕)', '(｡♥‿♥｡)', '♪(´▽｀)', '(⌒▽⌒)', '☆⌒(≧▽°)',
                '(￣▽￣)~*', '(*^ω^*)', '(o^∀^)', '♪(´ε｀ )', '(≧∇≦)ﾉ'
            ],
            'love': [
                '(❤´艸｀❤)', '(づ｡◕‿‿◕｡) づ', '(💕ω💕)', '♥(ˆ⌣ˆԅ)', '(❤️´艸｀❤️)',
                '(💖ω💖)', '(♥ω♥*)', '♥(･ω･ﾉ)', '(❤ω❤)', '(´∀❤)',
                '(💕´ ∀ `💕)', '(♥∀♥)', '♥(￣∀￣♥)', '(❤∀❤)', '♥(´∀人)'
            ],
            'angry': [
                '(╯°□°）╯︵ ┻━┻', '(╬▔皿▔) 凸', '（‵□′）', '(┻━┻︵╰(‵□′╰)', '┻━┻ミヽ (ಠ益ಠ) ﾉ︵ ┻━┻',
                '(╬￣皿￣)', '（╯°□°）╯', '(┻┻)(╰-_-╰)', '┻━┻ ︵ ヽ (°□° ヽ)', '凸 (¬‿¬) 凸'
            ],
            'sad': [
                '(；′⌒`)', '(T_T)', '(；ω；)', '(｡•́︿•̀｡)', '(qwq)',
                '(qwq;)', '(T▽T)', '(；′⌒`)', '(｡•́︿•̀｡)', '(；ω；`)',
                '(qwq)', '(T_T;)', '(；′⌒`)', '(｡•́︿•̀｡)', '(；ω；)'
            ],
            'shy': [
                '(⁄ ⁄•⁄ω⁄•⁄ ⁄)', '(*/ω＼*)', '(⁄ ⁄•⁄▽⁄•⁄ ⁄)', '(◡‿◡✿)', '(✿◡‿◡)',
                '(//▽//)', '(⁄ ⁄•⁄ω⁄•⁄ ⁄)', '(*/ω＼*)', '(✿◠‿◠)', '(｡･ω･｡)'
            ],
            'curious': [
                '(・ω・?)', '(・_・?)', '(￣ω￣?)', '(・∀・?)', '(・へ・?)',
                '(・ω・｀)', '(￣ω￣;)', '(・_・;)', '(・∀・｀)', '(￣_￣)'
            ],
            'excited': [
                '(★^O^★)', '(☆▽☆)', '(★ω★)', '(✪ω✪)', '(★▽★)',
                '(☆ω☆)', '(★∀★)', '(✪∀✪)', '(☆∀☆)', '(★∀人)'
            ],
            'surprised': [
                '(⊙_⊙;)', '(°ロ°) !', '(ﾟДﾟ;)', '(⊙x⊙;)', '(°Д°≡°Д°)',
                '(⊙.⊙)', '(°ロ°)', '(ﾟДﾟ≡ﾟДﾟ)', '(⊙x⊙)', '(°Д°)'
            ],
            'thinking': [
                '(・ω・｀)', '(￣ω￣;)', '(・_・;)', '(・∀・｀)', '(￣_￣)',
                '(￣ー￣)', '(・ω・｀)', '(￣ω￣;)', '(・_・;)', '(￣∇￣)'
            ],
            'laughing': [
                '(￣▽￣)~*', '(≧∇≦)', '(^_-)-☆', '(⌒_⌒;)', '(￣y▽,￣)',
                '(≧∇≦) ﾉ', '(￣▽￣)~*', '(^_-)-☆', '(⌒_⌒;)', '(☆▽☆)'
            ],
            'crying': [
                '(T_T)', '(；′⌒`)', '(qwq)', '(；ω；)', '(T▽T)',
                '(T_T;)', '(；′⌒`)', '(qwq)', '(；ω；)', '(qwq;)'
            ],
            'proud': [
                '(￣▽￣) ノ', '(^_-)-☆', '(￣ω￣)', '(・∀・)', '(￣y▽,￣)',
                '(￣▽￣)~*', '(^_-)-☆', '(￣ω￣)', '(・∀・)', '(☆∀☆)'
            ],
            'embarrassed': [
                '(//▽//)', '(⁄ ⁄•⁄ω⁄•⁄ ⁄)', '(*/ω＼*)', '(//ω//)', '(⁄ ⁄•⁄▽⁄•⁄ ⁄)',
                '(//▽//)', '(⁄ ⁄•⁄ω⁄•⁄ ⁄)', '(*/ω＼*)', '(//ω//)', '(｡･ω･｡)'
            ],
            'cool': [
                '(￣^￣)', '(・ω・)~', '(￣ω￣)', '(￣ω￣;)', '(・∀・｀)',
                '(￣^￣)', '(・ω・)~', '(￣ω￣)', '(￣ω￣;)', '(・∀・)'
            ],
            'other': [
                '(・ω・)', '(￣ω￣)', '(・_・)', '(・∀・)', '(￣▽￣)',
                '(・ω・)', '(￣ω￣)', '(・_・)', '(・∀・)', '(￣▽￣)'
            ]
        }

        self.screenshot_dir = os.path.join(root_dir, 'screenshot')

    def _load_emotion_types_from_directory(self) -> List[str]:
        """从表情包目录动态加载所有支持的表情类型"""
        emotion_types = ['other']  # 默认类型
        
        if not os.path.exists(self.emoji_dir):
            logger.warning(f"表情包目录不存在：{self.emoji_dir}")
            return emotion_types
        
        try:
            # 遍历表情包目录，获取所有子目录名称作为表情类型
            for item in os.listdir(self.emoji_dir):
                item_path = os.path.join(self.emoji_dir, item)
                if os.path.isdir(item_path):
                    # 检查目录中是否有图片文件
                    has_images = any(
                        f.lower().endswith(('.gif', '.jpg', '.png', '.jpeg'))
                        for f in os.listdir(item_path)
                    )
                    if has_images and item not in emotion_types:
                        emotion_types.append(item)
            
            logger.info(f"已加载 {len(emotion_types)} 种表情类型：{emotion_types}")
        except Exception as e:
            logger.error(f"加载表情类型失败：{str(e)}")
        
        return emotion_types

    def select_kaomoji_position(self) -> str:
        """根据权重选择颜文字插入位置"""
        position = random.choices(
            self.kaomoji_positions,
            weights=self.position_weights,
            k=1
        )[0]
        return position

    def insert_kaomoji_into_text(self, text: str, kaomoji: str, emotion_type: str) -> str:
        """将颜文字插入到文本中
        
        Args:
            text: 原始文本
            kaomoji: 颜文字
            emotion_type: 情绪类型
            
        Returns:
            str: 插入颜文字后的文本
        """
        position = self.select_kaomoji_position()
        
        if position == 'start':
            # 在开头插入
            return f"{kaomoji} {text}"
        elif position == 'middle':
            # 在中间插入（找第一个句号或逗号）
            for sep in ['。', '，', '！', '？', '.', ',', '!', '?']:
                if sep in text:
                    parts = text.split(sep, 1)
                    if len(parts) == 2:
                        return f"{parts[0]}{sep} {kaomoji} {parts[1]}"
            # 如果没有找到分隔符，在中间位置插入
            mid = len(text) // 2
            return f"{text[:mid]} {kaomoji} {text[mid:]}"
        else:
            # 在结尾插入（默认）
            return f"{text} {kaomoji}"

    def process_text_with_kaomoji(self, text: str, emotion_type: str = 'other', intensity: float = 0) -> str:
        """处理文本，根据情绪添加颜文字
        
        Args:
            text: 原始文本
            emotion_type: 情绪类型
            intensity: 情绪强度
            
        Returns:
            str: 处理后的文本（可能包含颜文字）
        """
        # 判断是否应该添加颜文字
        if self.should_send_kaomoji(emotion_type, intensity):
            kaomoji = self.get_kaomoji(emotion_type)
            if kaomoji:
                # 将颜文字插入到文本中
                processed_text = self.insert_kaomoji_into_text(text, kaomoji, emotion_type)
                logger.info(f"已添加颜文字：{kaomoji}")
                return processed_text
        
        return text

    def detect_emotion_intensity(self, text: str) -> Tuple[str, float]:
        """检测情绪强度和类型
        
        Args:
            text: 要分析的文本
            
        Returns:
            Tuple[str, float]: (情绪类型，强度 0-1)
        """
        text_lower = text.lower()
        max_intensity = 0.0
        detected_emotion = 'other'
        
        # 定义详细的情绪关键词映射
        emotion_keywords = {
            'happy': ['开心', '高兴', '快乐', '愉快', '欣喜', '喜悦', '欣慰', '满足', '满意', '舒服'],
            'love': ['喜欢', '爱', '爱你', '爱你哦', '喜欢', '钟意', '心动', '心动了', '好喜欢'],
            'angry': ['生气', '愤怒', '恼火', '气愤', '不爽', '讨厌', '烦', '烦死了', '气死', '无语'],
            'sad': ['难过', '伤心', '悲痛', '哭泣', '流泪', '委屈', '失落', '失望', '沮丧', '郁闷'],
            'shy': ['害羞', '羞羞', '脸红', '不好意思', '腼腆', '害臊', '难为情'],
            'curious': ['好奇', '想知道', '为什么', '怎么回事', '什么', '咋', '咦', '嗯？', '啊？'],
            'excited': ['激动', '兴奋', '期待', '盼望', '迫不及待', '太棒了', '太好了', '太酷了'],
            'surprised': ['惊讶', '吃惊', '震惊', '意外', '居然', '竟然', '天哪', '哇塞', '天啊'],
            'laughing': ['哈哈', '嘻嘻', '嘿嘿', '笑死', '好笑', '逗我', '乐', '笑'],
            'crying': ['哭', '哭了', '想哭', '泪', '泪了', '呜呜', '呜咽', '抽泣'],
            'proud': ['骄傲', '自豪', '厉害', '牛', '牛逼', '666', '优秀', '棒', '厉害'],
            'embarrassed': ['尴尬', '糗', '出丑', '丢脸', '丢人', '社死', '好尴尬'],
            'cool': ['酷', '帅', '潇洒', '威风', '霸气', '有范儿', '有型'],
        }
        
        # 检查极端情绪关键词
        for emotion_type, keywords in self.extreme_emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # 极端情绪，返回高概率
                    return (emotion_type, 1.0)
        
        # 检查普通情绪关键词
        best_match_score = 0
        for emotion_type, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # 计算匹配分数
                    score = text_lower.count(keyword) * 0.2
                    # 根据标点符号增强强度
                    if any(p in text for p in ['！！！', '！！', '！！！']):
                        score = min(1.0, score + 0.3)
                    elif any(p in text for p in ['!!', '!', '！！！', '！！']):
                        score = min(1.0, score + 0.2)
                    elif any(p in text for p in ['...', '。。.']):
                        score = min(1.0, score + 0.1)
                    
                    if score > best_match_score:
                        best_match_score = score
                        detected_emotion = emotion_type
        
        # 如果没有匹配到情绪关键词，检查表情标签
        if detected_emotion == 'other':
            tags = self.extract_emotion_tags(text)
            if tags:
                detected_emotion = tags[0]
                max_intensity = 0.5
                # 如果有多个表情标签，强度更高
                if len(tags) >= 2:
                    max_intensity = max(max_intensity, 0.7)
        else:
            max_intensity = best_match_score
        
        # 如果仍然没有检测到情绪，返回默认值
        if detected_emotion == 'other' and max_intensity == 0:
            # 检查是否有感叹号等表示情绪的标点
            if any(p in text for p in ['！！！', '！！', '！！！']):
                max_intensity = 0.3
            elif any(p in text for p in ['!!', '!', '...']):
                max_intensity = 0.2
        
        return (detected_emotion, max_intensity)

    def should_send_emoji(self, emotion_type: str = None, intensity: float = 0) -> bool:
        """判断是否应该发送表情包
        
        Args:
            emotion_type: 情绪类型
            intensity: 情绪强度 (0-1)
            
        Returns:
            bool: 是否发送表情包
        """
        # 基础概率判断
        if random.random() < self.emoji_probability:
            return True
        return False

    def should_send_kaomoji(self, emotion_type: str = None, intensity: float = 0) -> bool:
        """判断是否应该发送颜文字
        
        Args:
            emotion_type: 情绪类型
            intensity: 情绪强度 (0-1)
            
        Returns:
            bool: 是否发送颜文字
        """
        # 基础概率判断
        if random.random() < self.kaomoji_probability:
            return True
        
        # 极端情绪时提高概率
        if intensity >= 0.7 and random.random() < self.extreme_emotion_probability:
            return True
        
        return False

    def get_kaomoji(self, emotion_type: str = 'other') -> str:
        """获取颜文字
        
        Args:
            emotion_type: 情绪类型
            
        Returns:
            str: 颜文字
        """
        # 获取对应情绪的表情列表
        emoji_list = self.kaomoji_map.get(emotion_type, self.kaomoji_map['other'])
        return random.choice(emoji_list)

    def extract_emotion_tags(self, text: str) -> list:
        """从文本中提取表情标签
        
        支持以下格式：
        - [happy] - 英文标签
        - [高兴] - 中文标签
        - [开心] - 中文别名
        - 文本中的关键词如"好开心"、"生气了"等
        """
        tags = []
        
        # 首先尝试提取方括号内的标签
        start = 0
        while True:
            start = text.find('[', start)
            if start == -1:
                break
            end = text.find(']', start)
            if end == -1:
                break
            tag = text[start+1:end].strip().lower()
            # 使用关键词映射模块查找表情类型
            emotion_type = emoji_keyword_handler.get_emotion_type(tag)
            if emotion_type and emotion_type in self.emotion_types:
                tags.append(emotion_type)
                logger.info(f"检测到表情标签：{tag} -> {emotion_type}")
            start = end + 1
        
        # 如果没有找到标签，尝试在文本中查找关键词
        if not tags:
            emotion_type = emoji_keyword_handler.find_emotion_in_text(text)
            if emotion_type and emotion_type in self.emotion_types:
                tags.append(emotion_type)
                logger.info(f"检测到关键词表情：{emotion_type}")
        
        return tags

    def select_emotion(self, text: str) -> str:
        """根据文本内容选择最合适的表情类型
        
        Args:
            text: 要分析的文本
            
        Returns:
            str: 表情类型
        """
        # 首先尝试从文本中提取表情标签
        tags = self.extract_emotion_tags(text)
        if tags:
            return tags[0]
        
        # 如果没有标签，根据文本内容判断情绪
        emotion, intensity = self.detect_emotion_intensity(text)
        
        # 如果检测到情绪，返回对应类型
        if emotion != 'other' or intensity > 0.5:
            return emotion
        
        # 默认返回其他
        return 'other'

    def select_emoji(self, emotion_type: str = None) -> Optional[str]:
        """根据情绪类型选择表情包文件
        
        Args:
            emotion_type: 情绪类型，如果为 None 则随机选择
            
        Returns:
            Optional[str]: 表情包文件路径，如果找不到则返回 None
        """
        # 如果没有指定情绪类型，随机选择一个
        if emotion_type is None:
            if len(self.emotion_types) > 1:
                emotion_type = random.choice(self.emotion_types[1:])  # 排除 'other'
            else:
                emotion_type = 'other'
        
        # 尝试使用指定的情绪类型
        emoji_path = self._find_emoji_file(emotion_type)
        if emoji_path:
            logger.info(f"已选择 {emotion_type} 表情包：{emoji_path}")
            return emoji_path
        
        # 如果找不到，尝试使用其他类型
        if emotion_type != 'other':
            emoji_path = self._find_emoji_file('other')
            if emoji_path:
                logger.info(f"使用其他表情包：{emoji_path}")
                return emoji_path
        
        return None

    def _find_emoji_file(self, emotion_type: str) -> Optional[str]:
        """在指定情绪类型的目录中查找表情包文件
        
        Args:
            emotion_type: 情绪类型
            
        Returns:
            Optional[str]: 表情包文件路径，如果找不到则返回 None
        """
        if not os.path.exists(self.emoji_dir):
            return None
        
        emotion_dir = os.path.join(self.emoji_dir, emotion_type)
        if not os.path.exists(emotion_dir):
            return None
        
        # 查找所有图片文件
        emoji_files = [
            f for f in os.listdir(emotion_dir)
            if f.lower().endswith(('.gif', '.jpg', '.png', '.jpeg'))
        ]
        
        if not emoji_files:
            return None
        
        # 随机选择一个表情包
        selected_file = random.choice(emoji_files)
        return os.path.join(emotion_dir, selected_file)

    def send_emoji(self, emoji_path: str, chat_name: str, wx: WeChat):
        """发送表情包到微信
        
        Args:
            emoji_path: 表情包文件路径
            chat_name: 聊天对象名称
            wx: 微信实例
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(emoji_path):
                logger.error(f"表情包文件不存在：{emoji_path}")
                return
            
            # 发送表情包
            wx.SendFiles(filepath=emoji_path, friend=chat_name)
            logger.info(f"已发送表情包：{emoji_path}")
            
            # 添加小延迟，避免发送过快
            time.sleep(0.5)
            
        except Exception as e:
            logger.error(f"发送表情包失败：{str(e)}")

    def send_emoji_by_name(self, emotion_type: str, chat_name: str, wx: WeChat):
        """根据情绪类型发送表情包
        
        Args:
            emotion_type: 情绪类型
            chat_name: 聊天对象名称
            wx: 微信实例
        """
        emoji_path = self.select_emoji(emotion_type)
        if emoji_path:
            self.send_emoji(emoji_path, chat_name, wx)
        else:
            logger.warning(f"未找到 {emotion_type} 类型的表情包")

    def get_emoji_for_emotion(self, emotion_type: str) -> Optional[str]:
        """根据情绪类型获取表情包文件路径（兼容接口）
        
        Args:
            emotion_type: 情绪类型
            
        Returns:
            Optional[str]: 表情包文件路径，如果找不到则返回 None
        """
        return self.select_emoji(emotion_type)


