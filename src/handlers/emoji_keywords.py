"""
表情包关键词映射模块
提供表情包调用关键词的映射和别名支持

支持以下调用方式：
- [happy] - 英文标签
- [高兴] - 中文标签
- [开心] - 中文别名
- [嘻嘻] - 口语化关键词
"""

import re
from typing import Dict, List, Optional

# 表情包关键词映射表（关键词 -> 表情类型）
EMOJI_KEYWORD_MAP = {
    # === 高兴类 ===
    'happy': 'happy',
    '高兴': 'happy',
    '开心': 'happy',
    '开心了': 'happy',
    '快乐': 'happy',
    '喜悦': 'happy',
    '嘻嘻': 'happy',
    '哈哈': 'happy',
    '嘿嘿': 'happy',
    '笑': 'happy',
    '笑了': 'happy',
    '笑死': 'happy',
    '乐': 'happy',
    '乐呵': 'happy',
    '喜庆': 'happy',
    '得意': 'happy',
    '美滋滋': 'happy',
    '偷笑': 'happy',
    '窃喜': 'happy',
    
    # === 爱恋类 ===
    'love': 'love',
    '爱': 'love',
    '爱恋': 'love',
    '喜欢': 'love',
    '心动': 'love',
    '心动了': 'love',
    '害羞': 'shy',  # 爱恋相关
    '脸红': 'shy',  # 爱恋相关
    '害羞了': 'shy',
    '想你了': 'love',
    '想念': 'love',
    '抱抱': 'love',
    '拥抱': 'love',
    '亲亲': 'love',
    '么么哒': 'love',
    '啵啵': 'love',
    '爱心': 'love',
    '比心': 'love',
    '笔芯': 'love',
    '爱你': 'love',
    '喜欢你': 'love',
    '心动不已': 'love',
    '小鹿乱撞': 'love',
    
    # === 生气类 ===
    'angry': 'angry',
    '生气': 'angry',
    '愤怒': 'angry',
    '气': 'angry',
    '气死了': 'angry',
    '气死': 'angry',
    '气呼呼': 'angry',
    '气鼓鼓': 'angry',
    '恼火': 'angry',
    '火大': 'angry',
    '发火': 'angry',
    '炸毛': 'angry',
    '不爽': 'angry',
    '不爽了': 'angry',
    '哼': 'angry',
    '哼唧': 'angry',
    '咬牙切齿': 'angry',
    '火冒三丈': 'angry',
    '七窍生烟': 'angry',
    
    # === 悲伤类 ===
    'sad': 'sad',
    '悲伤': 'sad',
    '难过': 'sad',
    '伤心': 'sad',
    '伤心了': 'sad',
    '委屈': 'sad',
    '委屈了': 'sad',
    '哭': 'sad',
    '哭了': 'sad',
    '哭泣': 'sad',
    '流泪': 'sad',
    '落泪': 'sad',
    '泪目': 'sad',
    '呜呜': 'sad',
    '呜咽': 'sad',
    '抽泣': 'sad',
    '心酸': 'sad',
    '心碎': 'sad',
    '心碎了': 'sad',
    '好难过': 'sad',
    '太难了': 'sad',
    'emo': 'sad',
    'emo 了': 'sad',
    
    # === 好奇类 ===
    'curious': 'curious',
    '好奇': 'curious',
    '疑问': 'curious',
    '疑惑': 'curious',
    '困惑': 'curious',
    '不解': 'curious',
    '不懂': 'curious',
    '不明白': 'curious',
    '啥': 'curious',
    '啥呢': 'curious',
    '啥呀': 'curious',
    '什么': 'curious',
    '什么呢': 'curious',
    '为什么': 'curious',
    '为啥': 'curious',
    '咋': 'curious',
    '咋办': 'curious',
    '咋回事': 'curious',
    '咦': 'curious',
    '诶': 'curious',
    '嗯？': 'curious',
    '啊？': 'curious',
    '哈？': 'curious',
    '问号': 'curious',
    '满头问号': 'curious',
    '一脸懵': 'curious',
    '懵逼': 'curious',
    '懵了': 'curious',
    
    # === 害羞类 ===
    'shy': 'shy',
    '害羞': 'shy',
    '脸红': 'shy',
    '脸红了': 'shy',
    '不好意思': 'shy',
    '腼腆': 'shy',
    '羞涩': 'shy',
    '扭捏': 'shy',
    '害羞了': 'shy',
    '脸红红': 'shy',
    '羞羞': 'shy',
    '羞答答': 'shy',
    '害臊': 'shy',
    '难为情': 'shy',
    '小害羞': 'shy',
    '有点害羞': 'shy',
    
    # === 崇拜类 ===
    'admire': 'admire',
    '崇拜': 'admire',
    '佩服': 'admire',
    '敬佩': 'admire',
    '敬仰': 'admire',
    '尊敬': 'admire',
    '跪了': 'admire',
    '跪拜': 'admire',
    '膜拜': 'admire',
    '大佬': 'admire',
    '大神': 'admire',
    '厉害': 'admire',
    '厉害了': 'admire',
    '太强了': 'admire',
    '666': 'admire',
    '牛': 'admire',
    '牛批': 'admire',
    '牛逼': 'admire',
    '牛哇': 'admire',
    '牛啊': 'admire',
    '绝了': 'admire',
    '太强': 'admire',
    '惊了': 'admire',
    '震惊': 'admire',
    '惊讶': 'admire',
    '惊叹': 'admire',
    '哇塞': 'admire',
    '哇哦': 'admire',
    '哇': 'admire',
    
    # === 同意类 ===
    'agree': 'agree',
    '同意': 'agree',
    '好的': 'agree',
    '好': 'agree',
    '行': 'agree',
    '行吧': 'agree',
    '行行行': 'agree',
    '可以': 'agree',
    '没问题': 'agree',
    '收到': 'agree',
    '收到啦': 'agree',
    '嗯': 'agree',
    '嗯嗯': 'agree',
    '嗯呐': 'agree',
    '对': 'agree',
    '对的': 'agree',
    '没错': 'agree',
    '正确': 'agree',
    '赞同': 'agree',
    '赞成': 'agree',
    '认可': 'agree',
    'OK': 'agree',
    'ok': 'agree',
    'oK': 'agree',
    '👌': 'agree',
    '好的呀': 'agree',
    '好哒': 'agree',
    '好滴': 'agree',
    '好嘞': 'agree',
    '没问题': 'agree',
    '包在我身上': 'agree',
    '成交': 'agree',
    '一言为定': 'agree',
    
    # === 礼貌类 ===
    'polite': 'polite',
    '礼貌': 'polite',
    '谢谢': 'polite',
    '谢谢你': 'polite',
    '感谢': 'polite',
    '多谢': 'polite',
    '感恩': 'polite',
    '费心了': 'polite',
    '辛苦': 'polite',
    '辛苦了': 'polite',
    '辛苦啦': 'polite',
    '劳烦': 'polite',
    '有劳': 'polite',
    '拜托': 'polite',
    '拜托了': 'polite',
    '求': 'polite',
    '求求': 'polite',
    '求求了': 'polite',
    '拜托拜托': 'polite',
    
    # === 抱歉类 ===
    'polite': 'polite',  # 抱歉也归入礼貌类
    'sorry': 'polite',
    '抱歉': 'polite',
    '对不起': 'polite',
    '不好意思': 'polite',
    '抱歉了': 'polite',
    '抱歉抱歉': 'polite',
    '我的错': 'polite',
    '我错了': 'polite',
    '赔罪': 'polite',
    '赔礼': 'polite',
    '请原谅': 'polite',
    '谅解': 'polite',
    
    # === 鼓励类 ===
    'encourage': 'encourage',
    '鼓励': 'encourage',
    '加油': 'encourage',
    '加油加油': 'encourage',
    '打气': 'encourage',
    '支持': 'encourage',
    '支持你': 'encourage',
    '挺你': 'encourage',
    '为你加油': 'encourage',
    '别放弃': 'encourage',
    '坚持': 'encourage',
    '坚持住': 'encourage',
    '你可以的': 'encourage',
    '一定行': 'encourage',
    '一定可以的': 'encourage',
    '我相信你': 'encourage',
    '冲': 'encourage',
    '冲鸭': 'encourage',
    '冲啊': 'encourage',
    '上': 'encourage',
    '上上上': 'encourage',
    '干': 'encourage',
    '干巴': 'encourage',
    'fighting': 'encourage',
    'fight': 'encourage',
    '认真': 'encourage',
    '认真了': 'encourage',
    '努力': 'encourage',
    '用功': 'encourage',
    
    # === 等待类 ===
    'wait': 'wait',
    '等待': 'wait',
    '等': 'wait',
    '等等': 'wait',
    '等一下': 'wait',
    '等一会': 'wait',
    '等会儿': 'wait',
    '稍等': 'wait',
    '稍等下': 'wait',
    '稍候': 'wait',
    '稍等一下': 'wait',
    '等一下下': 'wait',
    '别急': 'wait',
    '别着急': 'wait',
    '慢慢来': 'wait',
    '不着急': 'wait',
    '耐心': 'wait',
    '耐心点': 'wait',
    '等等我': 'wait',
    '等我': 'wait',
    
    # === 问候类 ===
    'greeting': 'greeting',
    '问候': 'greeting',
    '打招呼': 'greeting',
    '你好': 'greeting',
    '您好': 'greeting',
    '嗨': 'greeting',
    'hi': 'greeting',
    'hello': 'greeting',
    '早': 'greeting',
    '早上': 'greeting',
    '早上好': 'greeting',
    '早安': 'greeting',
    '早啊': 'greeting',
    '早呀': 'greeting',
    '午安': 'greeting',
    '下午好': 'greeting',
    '晚': 'greeting',
    '晚上': 'greeting',
    '晚上好': 'greeting',
    '晚安': 'greeting',
    '好梦': 'greeting',
    '好眠': 'greeting',
    '拜拜': 'greeting',
    '再见': 'greeting',
    '再会': 'greeting',
    '回见': 'greeting',
    '回头见': 'greeting',
    '下次见': 'greeting',
    '改天见': 'greeting',
    '走了': 'greeting',
    '先走了': 'greeting',
    '溜了': 'greeting',
    '撤了': 'greeting',
    '拜': 'greeting',
    
    # === 饥饿类 ===
    'hungry': 'hungry',
    '饥饿': 'hungry',
    '饿': 'hungry',
    '饿了': 'hungry',
    '好饿': 'hungry',
    '太饿了': 'hungry',
    '饿死了': 'hungry',
    '饿扁了': 'hungry',
    '肚子饿': 'hungry',
    '肚子饿了': 'hungry',
    '想吃': 'hungry',
    '想吃东西': 'hungry',
    '觅食': 'hungry',
    '干饭': 'hungry',
    '干饭人': 'hungry',
    '吃饭': 'hungry',
    '吃饭了': 'hungry',
    '开饭': 'hungry',
    '开饭了': 'hungry',
    '饭饭': 'hungry',
    '我要吃饭': 'hungry',
    '饿狼传说': 'hungry',
    '饿虎扑食': 'hungry',
    '馋': 'hungry',
    '馋了': 'hungry',
    '嘴馋': 'hungry',
    '贪吃': 'hungry',
    '小吃货': 'hungry',
    '吃货': 'hungry',
    
    # === 疲倦类 ===
    'tired': 'tired',
    '疲倦': 'tired',
    '累': 'tired',
    '累了': 'tired',
    '好累': 'tired',
    '太累了': 'tired',
    '累死了': 'tired',
    '累瘫': 'tired',
    '累成狗': 'tired',
    '疲惫': 'tired',
    '疲乏': 'tired',
    '困': 'tired',
    '困了': 'tired',
    '好困': 'tired',
    '太困了': 'tired',
    '犯困': 'tired',
    '想睡觉': 'tired',
    '想睡': 'tired',
    '睡觉': 'tired',
    '睡觉': 'tired',
    '休息': 'tired',
    '休息一下': 'tired',
    '歇会儿': 'tired',
    '歇歇': 'tired',
    '躺平': 'tired',
    '摆烂': 'tired',
    '摸鱼': 'tired',
    '打工': 'tired',
    '打工人': 'tired',
    '搬砖': 'tired',
    '社畜': 'tired',
    '加班': 'tired',
    '熬夜': 'tired',
    '通宵': 'tired',
    '哈欠': 'tired',
    '打哈欠': 'tired',
    '眼皮打架': 'tired',
    '昏昏欲睡': 'tired',
    '无精打采': 'tired',
    '有气无力': 'tired',
    
    # === 想要类 ===
    'want': 'want',
    '想要': 'want',
    '想': 'want',
    '想要': 'want',
    '想得要命': 'want',
    '渴望': 'want',
    '盼望': 'want',
    '期待': 'want',
    '期望': 'want',
    '希望': 'want',
    '求求': 'want',
    '求求了': 'want',
    '想要嘛': 'want',
    '想要那个': 'want',
    '给我': 'want',
    '要': 'want',
    '要要要': 'want',
    '想要想要': 'want',
    '好想要': 'want',
    '超级想要': 'want',
    '特别想要': 'want',
    '非常想要': 'want',
    '馋死了': 'want',
    '眼馋': 'want',
    '眼巴巴': 'want',
    '眼热': 'want',
    '羡慕': 'want',
    
    # === 其他类 ===
    'other': 'other',
    '其他': 'other',
    '别的': 'other',
    '随便': 'other',
    '都行': 'other',
    '无所谓': 'other',
    '不知道': 'other',
    '无语': 'other',
    '无奈': 'other',
    '尴尬': 'other',
    '尴尬了': 'other',
    '社死': 'other',
    '社死现场': 'other',
    '无语凝噎': 'other',
    '汗': 'other',
    '汗颜': 'other',
    '冷汗': 'other',
    '冷汗直流': 'other',
    '黑线': 'other',
    '三条黑线': 'other',
    '扶额': 'other',
    '捂脸': 'other',
    '捂脸哭': 'other',
    '裂开': 'other',
    '心态崩了': 'other',
    '我裂开': 'other',
    '栓 Q': 'other',
    '我真的会谢': 'other',
    '6': 'other',
    '66': 'other',
    'emm': 'other',
    'emmm': 'other',
    'emmmm': 'other',
    '呃': 'other',
    '额': 'other',
    '呃啊': 'other',
    '唉': 'other',
    '哎': 'other',
    '哎呀': 'other',
    '哎哟': 'other',
    '嗷': 'other',
    '嗷呜': 'other',
    '喵': 'other',
    '喵呜': 'other',
    '汪': 'other',
    '汪汪': 'other',
}

# 表情类型到中文名称的映射
EMOTION_TYPE_NAMES = {
    'happy': '高兴',
    'love': '爱恋',
    'angry': '生气',
    'sad': '悲伤',
    'curious': '好奇',
    'shy': '害羞',
    'admire': '崇拜',
    'agree': '同意',
    'polite': '礼貌',
    'encourage': '鼓励',
    'wait': '等待',
    'greeting': '问候',
    'hungry': '饥饿',
    'tired': '疲倦',
    'want': '想要',
    'other': '其他',
}


class EmojiKeywordHandler:
    """表情包关键词处理器"""
    
    def __init__(self):
        self.keyword_map = EMOJI_KEYWORD_MAP
        self.type_names = EMOTION_TYPE_NAMES
    
    def get_emotion_type(self, keyword: str) -> Optional[str]:
        """根据关键词获取表情类型
        
        Args:
            keyword: 关键词（可以是英文标签或中文关键词）
            
        Returns:
            Optional[str]: 表情类型，如果找不到则返回 None
        """
        # 清理关键词
        keyword = keyword.strip().lower()
        
        # 移除方括号（如果存在）
        if keyword.startswith('[') and keyword.endswith(']'):
            keyword = keyword[1:-1].strip().lower()
        
        # 直接查找
        if keyword in self.keyword_map:
            return self.keyword_map[keyword]
        
        # 尝试部分匹配
        for k, v in self.keyword_map.items():
            if keyword in k or k in keyword:
                return v
        
        return None
    
    def find_emotion_in_text(self, text: str) -> Optional[str]:
        """在文本中查找表情关键词
        
        Args:
            text: 要分析的文本
            
        Returns:
            Optional[str]: 匹配到的表情类型，如果找不到则返回 None
        """
        text_lower = text.lower()
        
        # 首先尝试提取方括号内的标签
        tag_pattern = r'\[([^\]]+)\]'
        tags = re.findall(tag_pattern, text)
        for tag in tags:
            tag_clean = tag.strip().lower()
            if tag_clean in self.keyword_map:
                return self.keyword_map[tag_clean]
        
        # 然后在文本中查找关键词
        # 按关键词长度排序，优先匹配长关键词
        sorted_keywords = sorted(self.keyword_map.keys(), key=len, reverse=True)
        
        for keyword in sorted_keywords:
            if keyword in text_lower:
                return self.keyword_map[keyword]
        
        return None
    
    def get_type_name(self, emotion_type: str) -> str:
        """获取表情类型的中文名称
        
        Args:
            emotion_type: 表情类型
            
        Returns:
            str: 中文名称
        """
        return self.type_names.get(emotion_type, emotion_type)
    
    def get_all_keywords_for_type(self, emotion_type: str) -> List[str]:
        """获取某个表情类型的所有关键词
        
        Args:
            emotion_type: 表情类型
            
        Returns:
            List[str]: 关键词列表
        """
        keywords = []
        for k, v in self.keyword_map.items():
            if v == emotion_type:
                keywords.append(k)
        return keywords


# 创建全局实例
emoji_keyword_handler = EmojiKeywordHandler()


def get_emotion_type(keyword: str) -> Optional[str]:
    """便捷函数：根据关键词获取表情类型"""
    return emoji_keyword_handler.get_emotion_type(keyword)


def find_emotion_in_text(text: str) -> Optional[str]:
    """便捷函数：在文本中查找表情关键词"""
    return emoji_keyword_handler.find_emotion_in_text(text)


def get_type_name(emotion_type: str) -> str:
    """便捷函数：获取表情类型的中文名称"""
    return emoji_keyword_handler.get_type_name(emotion_type)