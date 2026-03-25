"""
生成表情包情感标签说明文件
根据情感分类生成中文标签说明
"""

import os
from pathlib import Path

# 情感分类及中文说明
EMOTION_LABELS = {
    'greeting': '问候 - 打招呼、告别类',
    'happy': '高兴 - 开心、喜悦类',
    'love': '爱恋 - 表达爱意类',
    'admire': '崇拜 - 惊叹、敬佩类',
    'polite': '礼貌 - 拜托、感谢类',
    'agree': '同意 - 认可、应答类',
    'angry': '生气 - 愤怒类',
    'sad': '悲伤 - 委屈、难过类',
    'shy': '害羞 - 羞怯类',
    'curious': '好奇 - 疑问、困惑类',
    'hungry': '饥饿 - 吃饭类',
    'tired': '疲倦 - 劳累、休息类',
    'encourage': '鼓励 - 加油、支持类',
    'want': '想要 - 渴望类',
    'wait': '等待 - 等候类',
    'sorry': '抱歉 - 道歉类',
    'grateful': '感激 - 感谢类',
}

def generate_labels_file(avatar_name, root_dir="d:/Fish-code/KouriChat"):
    """
    为指定角色生成标签说明文件
    
    Args:
        avatar_name: 角色名称
        root_dir: 项目根目录
    """
    emoji_dir = Path(root_dir) / "data" / "avatars" / avatar_name / "emojis"
    
    if not emoji_dir.exists():
        print(f"错误：表情包目录不存在 - {emoji_dir}")
        return
    
    # 生成说明内容
    content = []
    content.append("表情包情感标签说明")
    content.append("=" * 50)
    content.append("")
    
    # 按类别分组
    categories = {}
    for emotion, label in EMOTION_LABELS.items():
        category = label.split('-')[0]
        if category not in categories:
            categories[category] = []
        categories[category].append((emotion, label))
    
    # 生成各类别内容
    for category, emotions in sorted(categories.items()):
        content.append(f"【{category}类】")
        content.append("-" * 30)
        for emotion, label in sorted(emotions):
            # 获取该分类下的文件数量
            emotion_dir = emoji_dir / emotion
            file_count = len(list(emotion_dir.glob("*"))) if emotion_dir.exists() else 0
            content.append(f"  [{emotion}] - {label} ({file_count}个)")
        content.append("")
    
    # 添加使用说明
    content.append("使用说明")
    content.append("=" * 50)
    content.append("在聊天中使用 [情感标签] 格式发送表情包，例如:")
    content.append("  [happy] - 发送高兴类表情包")
    content.append("  [greeting] - 发送问候类表情包")
    content.append("")
    
    # 写入文件
    labels_file = emoji_dir / "标签说明.txt"
    with open(labels_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"[OK] 已生成标签说明：{labels_file}")


def main():
    """主函数"""
    avatars = ["AL_1S", "ATRI", "MONO", "Nijiko"]
    
    print("=" * 50)
    print("生成表情包标签说明工具")
    print("=" * 50)
    print("\n情感分类:")
    for emotion, label in EMOTION_LABELS.items():
        print(f"  [{emotion}] - {label}")
    
    print("\n" + "=" * 50)
    print("选择目标角色:")
    for i, avatar in enumerate(avatars, 1):
        print(f"  {i}. {avatar}")
    print(f"  {len(avatars)+1}. 所有角色")
    
    try:
        choice = input("\n请输入选项 (默认：1): ").strip()
        if not choice:
            choice = "1"
        
        if choice.isdigit():
            choice = int(choice)
            if choice <= len(avatars):
                generate_labels_file(avatars[choice - 1])
            elif choice == len(avatars) + 1:
                for avatar in avatars:
                    print(f"\n[处理角色：{avatar}]")
                    generate_labels_file(avatar)
            else:
                print("无效选项")
        else:
            target = choice
            if target in avatars:
                generate_labels_file(target)
            else:
                print(f"未知角色：{target}")
                print(f"可用角色：{', '.join(avatars)}")
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n发生错误：{e}")


if __name__ == "__main__":
    main()