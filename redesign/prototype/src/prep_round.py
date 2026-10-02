from PIL import Image
im = Image.open("../../images/21.jpg").convert("RGB")
# head centre: (370, 410) in the 720x791 grey crop -> original coordinates
k = 1600 / 720
cx, cy = 200 + 370 * k, 157 + 405 * k
half = 560
box = (int(cx - half), int(cy - half), int(cx + half), int(cy + half))
im.crop(box).resize((640, 640), Image.LANCZOS).save("portrait_round.jpg", quality=84, optimize=True, progressive=True)
print("centre", round(cx), round(cy), "box", box)
