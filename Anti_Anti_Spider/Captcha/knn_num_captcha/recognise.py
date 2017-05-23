#coding:utf-8

import os
import requests
from PIL import Image
import math,time

# 获取裁判文书网的验证码
def imagesget():
    os.mkdir('images')
    count=0
    while True:
        img=requests.get('http://wenshu.court.gov.cn/User/ValidateCode/{}'.format(count)).content
        with open('images/%s.jpeg'%count,'wb') as imgfile:
            imgfile.write(img)
        count+=1
        if(count==100):
            break


def convert_image(image):
    image=image.convert('L') # 灰度
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if pix<120:#灰度低于120 设置为 0
                image2.putpixel((x,y),0)
    # image2.save('L.png')#将灰度图存储下来看效果
    return image2

def cut_image(image):
    ''' 字符切割,根据黑色的连续性,当某一列出现黑色为标志,当黑色消失为结束点'''
    inletter=False
    foundletter=False
    letters=[]
    start=0
    end=0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if(pix==0):
                inletter=True
        if foundletter==False and inletter ==True:
            foundletter=True
            start=x
        if foundletter==True and inletter==False:
            end=x
            letters.append((start,end))
            foundletter=False
        inletter=False
    images=[]
    for letter in letters:
        img=image.crop((letter[0],0,letter[1],image.size[1]))
        # img.save(str(letter[0])+'.jpeg')#展示切割效果
        images.append(img)
    return images

def buildvector(image):
    ''' 图片转换成矢量,将二维的图片转为一维'''
    result={}
    count=0
    for i in image.getdata():
        result[count]=i
        count+=1
    return result


class CaptchaRecognize:
    def __init__(self):
        self.letters=['0','1','2','3','4','5','6','7','8','9']
        self.loadSet()

    def loadSet(self):
        self.imgset=[]
        for letter in self.letters:
            temp=[]
            for img in os.listdir('./icon/%s'%(letter)):
                temp.append(buildvector(Image.open('./icon/%s/%s'%(letter,img))))
            self.imgset.append({letter:temp})

    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):

        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                # print type(topvalue),topvalue,count,concordance2[word]
                topvalue += count * concordance2[word]
                # time.sleep(10)
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

    def recognise(self,image):
        image=convert_image(image)#二值化
        images=cut_image(image)#字符单独切割出来
        vectors=[]
        for img in images:
            vectors.append(buildvector(img))
        result=[]
        for vector in vectors:
            guess=[]
            for image in self.imgset:
                for letter,temp in image.items():
                    relevance=0
                    num=0
                    for img in temp:
                        relevance+=self.relation(vector,img)
                        num+=1
                    relevance=relevance/num
                    guess.append((relevance,letter))
            guess.sort(reverse=True)
            result.append(guess[0])
        return result

if __name__=='__main__':
    imageRecognize=CaptchaRecognize()

    # single
    img1 = Image.open("L.png")
    result = imageRecognize.recognise(img1)
    string = [''.join(item[1]) for item in result]
    print(string)

    """
    # multiple
    for pg in os.listdir('images'):
        print(pg)
        img1 = Image.open("images/{}".format(pg))
        result_abbr_full_892.md=imageRecognize.recognise(img1)
        string=[''.join(item[1]) for item in result_abbr_full_892.md]
        print(string)
    """
