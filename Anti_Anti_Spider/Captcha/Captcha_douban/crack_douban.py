import requests

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