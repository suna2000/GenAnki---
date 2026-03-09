#!/usr/bin/env python3
"""
genanki 示例：生成 Anki 闪卡牌组
"""

import genanki
import random
import os

# 生成唯一的 ID
def generate_id():
    return random.randrange(1 << 30, 1 << 31)


# 创建牌组
my_deck = genanki.Deck(
    2059400110,
    '') #可选 养生保健 包罗万象 思维逻辑 技术知识 教员语录 段子来了 生活场景

# 创建模型
my_model = genanki.Model(
    1607392319,
    '简单模型',
    fields=[
        {'name': '问题'},
        {'name': '答案'},
    ],
    templates=[
        {
            'name': '卡片 1',
            'qfmt': '{{问题}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{答案}}',
        },
    ])

# 从 txt 文件读取笔记数据
# 文件格式：第一列为问题，第二列为回答，使用 Tab 分隔
notes_data = []
txt_file = os.path.join(os.path.dirname(__file__), 'note.txt')

if os.path.exists(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    question = parts[0]
                    answer = parts[1]
                    notes_data.append((question, answer))
else:
    print(f'错误: 找不到文件 {txt_file}')
    print('请创建 note.txt 文件，第一列为问题，第二列为回答，使用 Tab 分隔')
    exit(1)

# 将数据添加到牌组
for question, answer in notes_data:
    my_note = genanki.Note(
        model=my_model,
        fields=[question, answer])
    my_deck.add_note(my_note)

# 创建输出目录
output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(output_dir, exist_ok=True)

# 导出为 .apkg 文件
output_path = os.path.join(output_dir, 'my_notes.apkg')
genanki.Package(my_deck).write_to_file(output_path)

print(f'成功生成牌组！')
print(f'文件位置: {output_path}')
print(f'共生成 {len(my_deck.notes)} 张卡片')
print('')
print('使用方法:')
print('1. 打开 Anki')
print('2. 选择 File -> Import...')
print(f'3. 选择文件: {output_path}')