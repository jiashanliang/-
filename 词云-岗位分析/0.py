from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np


# https://blog.csdn.net/qq_24076135/article/details/78530885


text = """
.S. President Donald Trump1 arrived in Beijing Wednesday afternoon, beginning his three-day state visit to China.
It is Trump's first visit to the country since he assumed the presidency2 in January. He is the first head of state to visit China since the landmark3 19th National Congress of the Communist Party of China.
During his stay in Beijing, Trump will hold talks with Chinese President Xi Jinping and meet with other Chinese leaders.
Xi and Trump will hold strategic communications on significant issues of common concern to build new consensus4, enhance mutual5 understanding and friendship, and promote bilateral6 relations in all spheres, according to Vice7 Foreign Minister Zheng Zeguang.
Apart from formal activities commensurate with a state visit, "informal interactions" will be arranged for the presidents of the two countries, Zheng said.
This is the third meeting between Xi and Trump following their first meeting at Mar-a-Lago, Florida in April and the second in Hamburg, Germany on the sidelines of the G20 summit in July.
This year marks the 45th anniversary of former U.S. President Richard Nixon's "ice-breaking" visit to China, which began the normalization8 of relations between the two countries.
"""

mask_color_path = "people.jpg"  # 设置背景图片路径
font_path = 'simkai.ttf'  # 为matplotlib设置中文字体路径没;路径需要改成你本地的字体路径,若是全英文,也可不设字体路径
imgname1 = "en_WordCloud_DefautColors.png"  # 保存的图片名字1(只按照背景图片形状)
imgname2 = "en_WordCloud_ColorsByImg.png"  # 保存的图片名字2(颜色按照背景图片颜色布局生成)
width = 1000
height = 860
margin = 2
# 设置背景图片

if '.png' in mask_color_path:
    mask_coloring = plt.imread(mask_color_path) * 255
    mask_coloring = mask_coloring.astype(np.uint8)
else:
    mask_coloring = plt.imread(mask_color_path)

wc = WordCloud(font_path=font_path,
               background_color="white",  # 背景颜色
               max_words=200,  # 词云显示的最大词数
               mask=mask_coloring,  # 设置背景图片
               max_font_size=200,  # 字体最大值
               # random_state=42,
               width=width, height=height, margin=margin,
               )

with open('jobdetail.txt', 'r', encoding='utf-8') as fp:
    txt = fp.read()

f = ''.join(txt)
wc.generate(txt)
plt.figure()
# 以下代码显示图片
# 绘制词云
plt.imshow(wc)
plt.axis("off")
plt.show()

# 保存图片
wc.to_file(imgname1)

# 获得背景图的颜色
img_color = ImageColorGenerator(mask_coloring)
wc.recolor(color_func=img_color)
plt.figure()
# 以下代码显示图片
# 绘制词云
plt.imshow(wc)
plt.axis("off")
plt.show()

# 保存图片
wc.to_file(imgname2)
