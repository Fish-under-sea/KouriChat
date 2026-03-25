"""
表情包批量分类脚本
将 C:/Users/Fish/Downloads/表情包 下的表情包按情感分类到所有角色目录
根据文件名注释自动分类
"""

import os
import shutil
from pathlib import Path

# 源目录
SOURCE_DIR = "C:/Users/Fish/Downloads/表情包"

# 目标角色目录
TARGET_AVATARS = ["AL_1S", "ATRI", "MONO", "Nijiko"]

# 简化的情感分类及对应关键词
EMOTION_CATEGORIES = {
    'greeting': ['打招呼', '早安', '晚安', '再见', '再见 2', '再见 3'],
    'happy': ['高兴', '开心', '哈哈', '恭喜'],
    'love': ['爱恋', '拥抱', '想念'],
    'admire': ['崇拜', '超级崇拜', '惊叹', '惊讶'],
    'polite': ['拜托', '抱歉', '感谢', '辛苦了', '赞同'],
    'agree': ['好的', '收到', '嗯嗯', 'ok'],
    'angry': ['生气'],
    'sad': ['委屈', '要哭了'],
    'shy': ['害羞'],
    'curious': ['疑问', '懵逼'],
    'hungry': ['贪吃', '吃饭'],
    'tired': ['累了', '好困', '休息', '打工', '摸鱼'],
    'encourage': ['鼓励', '认真', '求求', '婉拒'],
    'want': ['想要'],
    'wait': ['等等'],
    'sorry': ['抱歉'],
    'grateful': ['感谢', '辛苦了'],
}

# 文件到情感的映射（基于文件名）
FILE_TO_EMOTION = {}

def build_file_emotion_map():
    """构建文件名到情感的映射"""
    for emotion, keywords in EMOTION_CATEGORIES.items():
        for keyword in keywords:
            if keyword not in FILE_TO_EMOTION:
                FILE_TO_EMOTION[keyword] = emotion

def detect_emotion_from_filename(filename):
    """根据文件名检测情感类型"""
    # 去掉扩展名
    name_without_ext = os.path.splitext(filename)[0]
    
    # 精确匹配
    if name_without_ext in FILE_TO_EMOTION:
        return FILE_TO_EMOTION[name_without_ext]
    
    # 部分匹配
    for keyword, emotion in FILE_TO_EMOTION.items():
        if keyword in name_without_ext:
            return emotion
    
    # 默认分类
    return 'other'

def sort_emojis_to_all_avatars(root_dir="d:/Fish-code/KouriChat"):
    """
    将表情包分类到所有角色目录
    
    Args:
        root_dir: 项目根目录
    """
    # 构建文件到情感的映射
    build_file_emotion_map()
    
    # 统计信息
    total_stats = {}
    total_copied = 0
    
    # 遍历源目录中的所有文件
    if not os.path.exists(SOURCE_DIR):
        print(f"错误：源目录不存在 - {SOURCE_DIR}")
        return
    
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f))]
    print(f"\n找到 {len(files)} 个表情包文件")
    print(f"需要分类到 {len(TARGET_AVATARS)} 个角色目录")
    print("=" * 50)
    
    for filename in files:
        source_path = os.path.join(SOURCE_DIR, filename)
        
        # 检测情感类型
        emotion = detect_emotion_from_filename(filename)
        
        # 复制到每个角色目录
        for target_avatar in TARGET_AVATARS:
            emoji_dir = Path(root_dir) / "data" / "avatars" / target_avatar / "emojis"
            emotion_dir = emoji_dir / emotion
            emotion_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = emotion_dir / filename
            shutil.copy2(source_path, dest_path)
        
        # 统计
        if emotion not in total_stats:
            total_stats[emotion] = 0
        total_stats[emotion] += 1
        total_copied += 1
        
        print(f"[OK] {filename} -> {emotion}/ (已复制到 {len(TARGET_AVATARS)} 个角色)")
    
    # 打印统计
    print("\n" + "=" * 50)
    print("分类统计 (每个角色):")
    for emotion, count in sorted(total_stats.items()):
        print(f"  {emotion}: {count} 个")
    print(f"\n总计：{total_copied} 个表情包已分类")
    print(f"总复制次数：{total_copied * len(TARGET_AVATARS)} 次")


def main():
    """主函数"""
    print("=" * 50)
    print("表情包批量分类工具")
    print("=" * 50)
    print(f"\n源目录：{SOURCE_DIR}")
    print(f"目标角色：{', '.join(TARGET_AVATARS)}")
    
    try:
        sort_emojis_to_all_avatars()
        print("\n分类完成!")
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()