import os
from PIL import Image, ImageDraw, ImageFont

background_color = "white"  # 背景
card_width = 180  # 卡片宽度
card_height = 240  # 卡片高度
margin = 20  # 边距
border_width = 2  # 边框粗细
corner_radius = 10  # 圆角半径
corner_type = 1  # 0为直角，1为圆角
os.makedirs("cards", exist_ok=True)

def load_suit_images():
    suit_images = []
    suit_files = ["黑桃.png", "红心.png", "方片.png", "草花.png"]
    for file_name in suit_files:
        suit_image = Image.open(file_name)
        suit_image.thumbnail((card_width - 2 * border_width, card_height - 2 * border_width))
        suit_images.append(suit_image)
    return suit_images

def create_deck_image():
    deck_image = Image.new(
        'RGB', (card_width * 13 + margin * 2, card_height * 4 + margin * 2), background_color
    )
    draw = ImageDraw.Draw(deck_image)
    font = ImageFont.truetype('arial.ttf', size=20)

    deck_rect = (border_width, border_width, deck_image.width - border_width - 1, deck_image.height - border_width - 1)
    if corner_type == 0:
        draw.rectangle(deck_rect, outline='black', width=border_width)
    else:
        draw.rounded_rectangle(deck_rect, corner_radius, outline='black', width=border_width)

    suit_images = load_suit_images()

    for i in range(4):
        for j in range(13):
            top = margin + i * card_height
            left = margin + j * card_width
            right = left + card_width
            bottom = top + card_height

            card_image = Image.new('RGB', (card_width, card_height), background_color)
            card_draw = ImageDraw.Draw(card_image)

            card_rect = (border_width, border_width, card_width - border_width - 1, card_height - border_width - 1)
            if corner_type == 0:
                card_draw.rectangle(card_rect, outline='black', width=border_width)
            else:
                card_draw.rounded_rectangle(card_rect, corner_radius, outline='black', width=border_width)

            if i == 3 and j > 10:
                fill_color = 'red' if j == 11 else 'black'
                card_name = 'JOKER'
                file_name = f'{card_name}_{j - 10}'
            else:
                card_name = get_card_name(j, i)
                fill_color = get_font_color(i)
                file_name = card_name

            card_draw.text((10, 10), card_name, font=font, fill=fill_color)
            card_image.paste(suit_images[i], (0, 0), mask=suit_images[i])

            deck_image.paste(card_image, (left, top))

            card_image.save(f'cards/{file_name}.png')

    return deck_image

def get_card_name(number, suit):
    suits = ['♠', '♥', '♦', '♣']
    numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return f"{numbers[number]}{suits[suit]}"

def get_font_color(suit):
    colors = ["black","red","red","black"]
    return colors[suit]

# 保存整副牌
def save_deck_image():
    deck_image = create_deck_image()
    deck_image.save('deck_of_cards.png')

# 单独导出每张牌
def export_individual_cards():
    os.makedirs("cards", exist_ok=True)
    create_deck_image()

if __name__ == '__main__':
    save_deck_image()
    export_individual_cards()