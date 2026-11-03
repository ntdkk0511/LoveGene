import os
from PIL import Image

# パス設定（Lib/images/dialogue_box.png）
script_dir = os.path.dirname(__file__)
image_path = os.path.abspath(os.path.join(script_dir, "..", "Lib", "images", "dialogue_box.png"))

if not os.path.exists(image_path):
    print(f"エラー: 画像が見つかりません -> {image_path}")
    exit(1)

# 1. 元画像を読み込み
box_img = Image.open(image_path).convert("RGBA")

# 2. 1920x1080 の完全透明キャンバスを作成
canvas_w, canvas_h = 1920, 1080
canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

# 3. メッセージ枠の表示サイズ調整（画面幅の85%程度にリサイズ）
target_w = int(canvas_w * 0.85)
aspect_ratio = box_img.height / box_img.width
target_h = int(target_w * aspect_ratio)

resized_box = box_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

# 4. キャンバスの下部中央に配置（画面下端から 30px 上）
x = (canvas_w - target_w) // 2
y = canvas_h - target_h - 30

canvas.paste(resized_box, (x, y), resized_box)

# 5. 上書き保存
canvas.save(image_path)
print(f"【成功】{image_path} を画面サイズに合わせた透過画像へ調整・保存しました。")