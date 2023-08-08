import os
from PIL import Image, ImageDraw, ImageFont

背景颜色 = "white"  # 背景
卡片宽度 = 180  # 卡片宽度
卡片高度 = 240  # 卡片高度
边距 = 20  # 边距
边框粗细 = 2  # 边框粗细
圆角半径 = 10  # 圆角半径
圆角类型 = 1  # 0为直角，1为圆角
os.makedirs("牌组", exist_ok=True)

def 加载花色图片():
    花色图片群 = []
    花色文件 = ["黑桃.png", "红心.png", "方片.png", "草花.png"]
    for 文件名 in 花色文件:
        花色图片 = Image.open(文件名)
        花色图片.thumbnail((卡片宽度 - 2 * 边框粗细, 卡片高度 - 2 * 边框粗细))
        花色图片群.append(花色图片)
    return 花色图片群

def 创建牌组图片():
    牌组图片 = Image.new(
        'RGB', (卡片宽度 * 13 + 边距 * 2, 卡片高度 * 4 + 边距 * 2), 背景颜色
    )
    绘制 = ImageDraw.Draw(牌组图片)
    字体 = ImageFont.truetype('arial.ttf', size=20)

    牌组矩形 = (边框粗细, 边框粗细, 牌组图片.width - 边框粗细 - 1, 牌组图片.height - 边框粗细 - 1)
    if 圆角类型 == 0:
        绘制.rectangle(牌组矩形, outline='black', width=边框粗细)
    else:
        绘制.rounded_rectangle(牌组矩形, 圆角半径, outline='black', width=边框粗细)

    花色图片 = 加载花色图片()

    for i in range(4):
        for j in range(13):
            顶部 = 边距 + i * 卡片高度
            左侧 = 边距 + j * 卡片宽度
            右侧 = 左侧 + 卡片宽度
            底部 = 顶部 + 卡片高度

            牌图片 = Image.new('RGB', (卡片宽度, 卡片高度), 背景颜色)
            牌绘制 = ImageDraw.Draw(牌图片)

            牌矩形 = (边框粗细, 边框粗细, 卡片宽度 - 边框粗细 - 1, 卡片高度 - 边框粗细 - 1)
            if 圆角类型 == 0:
                牌绘制.rectangle(牌矩形, outline='black', width=边框粗细)
            else:
                牌绘制.rounded_rectangle(牌矩形, 圆角半径, outline='black', width=边框粗细)

            if i == 3 and j > 10:
                填充颜色 = 'red' if j == 11 else 'black'
                牌名 = 'JOKER'
                文件名 = f'{牌名}_{j - 10}'
            else:
                牌名 = 获取牌名(j, i)
                填充颜色 = 获取字体颜色(i)
                文件名 = 牌名

            牌绘制.text((10, 10), 牌名, font=字体, fill=填充颜色)
            牌图片.paste(花色图片[i], (0, 0), mask=花色图片[i])

            牌组图片.paste(牌图片, (左侧, 顶部))

            牌图片.save(f'牌组/{文件名}.png')

    return 牌组图片

def 获取牌名(数字, 花色):
    花色列表 = ['♠', '♥', '♦', '♣']
    数字列表 = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return f"{数字列表[数字]}{花色列表[花色]}"

def 获取字体颜色(花色):
    颜色列表 = ["black","red","red","black"]
    return 颜色列表[花色]

# 保存整副牌
def 保存牌组图片():
    牌组图片 = 创建牌组图片()
    牌组图片.save('全部.png')

# 单独导出每张牌
def 导出单张牌():
    os.makedirs("牌组", exist_ok=True)
    创建牌组图片()

if __name__ == '__main__':
    保存牌组图片()
    导出单张牌()