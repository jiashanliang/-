# author: Xanto
# email: xanto@vip.163.com
# datetime: 2018/11/26 9:04
# software: PyCharm + Python3.6.2
# project_name: 数据分析职位分析


import jieba
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# Python+wordcloud+jieba+docx生成中文词云和词频统计
# https://blog.csdn.net/fengjianc/article/details/78929121

# 停用词词表 这里面的次都不会搜集到分词结果中
stopwords_path = 'stopwords1806.txt'

# 添加的自定义中文语句的代码在这里
# 添加的自定义中文语句的代码在这里
# 添加的自定义中文语句的代码在这里
jieba.add_word('数据分析')
jieba.add_word('用户画像')
jieba.add_word('本科')
jieba.add_word('专科')
jieba.add_word('硕士')
jieba.add_word('985')
jieba.add_word('211')

# 设置要分析的文本路径
text_path = 'job_description.txt'
text = open(text_path, encoding='utf-8').read()


# 封装jieba分词函数
def jiebaclearText(text):
    wordlist = []
    # 分词
    seg_list = jieba.cut(text, cut_all=False)
    # 拼接分词结果
    liststr = "/ ".join(seg_list)
    # 读取停用词
    with open(stopwords_path) as f:
        f_stop_text = f.read()
    # 分割停用词
    f_stop_seg_list = f_stop_text.split('\n')
    #  循环判断每个单词是否是停用词
    for word in liststr.split('/'):
        # 这里可以筛选最小字符长度
        # if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
        #     mywordlist.append(myword)
        if not (word.strip() in f_stop_seg_list):
            wordlist.append(word)
    return ''.join(wordlist)

# 返回分词结果
text = jiebaclearText(text)
print(text)

# 保存分词后的数据
with open('jobdetail.txt', 'w', encoding='utf-8') as fp:
    fp.write(text)
# 读取数据 这里之前是分两个文件的 所以有读写操作 可以自行去掉
with open('jobdetail.txt', 'r', encoding='utf-8') as fp:
    txt = fp.read()

# 背景图路径
mask_color_path = 'china.jpg'

# WordCloud默认是读取的jpg图像 如果是png要转换一下
if '.png' in mask_color_path:
    # 如果是png的就用numpy转换一下
    import numpy as np

    bg = plt.imread(mask_color_path) * 255
    bg = bg.astype(np.uint8)
else:
    bg = plt.imread(mask_color_path)

wc = WordCloud(background_color="white", mask=bg, font_path='simkai.ttf')
wc.generate(txt)
# 详细介绍见 https://blog.csdn.net/qq_24076135/article/details/78530885
# width,height,margin可以设置图片属性 使用背景图的话会以背景图的尺寸为准
# font_path设置字体集
# background_color参数为设置背景颜色,默认颜色为黑色


# 获得背景图的颜色
img_color = ImageColorGenerator(bg)
# 使用背景图的颜色
wc.recolor(color_func=img_color)
plt.figure()

# 如果设置背景无效：
#         1.使用背景图的颜色
#         2.切换jpg背景图

# 绘制词云
plt.imshow(wc)
plt.axis("off")
plt.show()

# 保存图片
wc.to_file('job.png')
