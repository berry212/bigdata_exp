import requests
import parsel
import re
import csv

f=open('二手房.csv',mode='w',encoding='utf-8',newline='')
csv_writer=csv.DictWriter(f,fieldnames=[
        '标题',
        '小区',
        '区域',
        '总价',
        '单价',
        '户型',
        '面积',
        '朝向',
        '装修',
        '楼层',
        '楼层数',
        '建筑',
])
csv_writer.writeheader()

#模拟浏览器
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}
for page in range(1,101):
    print(f'正在采集第{page}页的内容')

    #请求链接
    url=f'https://xa.lianjia.com/ershoufang/beilin/pg{page}/'

    #发送请求
    response=requests.get(url=url,headers=headers)


    #获取响应文本数据<网页源代码>
    html_data=response.text
    #把获取的字符串数据转换成可解析对象
    selector=parsel.Selector(html_data)
    #提取30个房源数据对应div标签
    divs=selector.css('.sellListContent li .info')
    #for循环遍历
    for div in divs:
        #提取具体数据内容
        title=div.css('.title a::text').get()#标题
        area_list=div.css('.positionInfo a::text').getall()
        area=area_list[0]#小区
        area_1 = area_list[1]  # 区域
        totalPrice=div.css('.totalPrice span::text').get()#总价
        unitPrice=div.css('.unitPrice span::text').get().replace('元/平','')#单价
        houseInfo = div.css('.houseInfo ::text').get().split(' | ')  # 信息
        houseType=houseInfo[0]#户型
        houseArea = houseInfo[1]#面积
        face=houseInfo[2]#朝向
        house = houseInfo[3]  #装修
        floor = houseInfo[4]  #楼层
        floor_1=houseInfo[4][0]
        floor_num=re.findall('\d+',floor)[0]
        building = houseInfo[5]  #建筑


        dit={
            '标题':title,
            '小区':area,
            '区域':area_1,
            '总价':totalPrice,
            '单价':unitPrice,
            '户型':houseType,
            '面积':houseArea,
            '朝向':face,
            '装修':house,
            '楼层':floor_1,
            '楼层数':floor_num,
            '建筑':building,
        }
        csv_writer.writerow(dit)

