from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

folder = Path(__file__).parent / "images"
folder.mkdir(exist_ok=True)

def make_button(filename, text, color):
    img = Image.new("RGBA", (480, 110), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        (4, 4, 475, 105),
        radius=20,
        fill=color,
        outline="white",
        width=3
    )

    font_path = "C:/Windows/Fonts/meiryo.ttc"
    font = ImageFont.truetype(font_path, 35)

    box = draw.textbbox((0, 0), text, font=font)
    x = (480 - (box[2] - box[0])) / 2 - box[0]
    y = (110 - (box[3] - box[1])) / 2 - box[1]

    draw.text((x, y), text, font=font, fill="white")

    img.save(folder / filename)

make_button(
    "consult.png",
    "アプローチ相談",
    "#2563EB"
)

make_button(
    "practice.png",
    "告白予行モード",
    "#475569"
)

print("ボタン画像を作成しました！")