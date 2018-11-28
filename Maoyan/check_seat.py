#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
                            _ooOoo_  
                           o8888888o  
                           88" . "88  
                          (|  -_-  |)  
                           O\  =  /O  
                        ____/`---'\____  
                      .   ' \\| |// `.  
                       / \\||| : |||// \  
                     / _||||| -:- |||||- \  
                       | | \\\ - /// | |  
                     | \_| ''\---/'' | |  
                      \ .-\__ `-` ___/-. /  
                   ___`. .' /--.--\ `. . __  
                ."" '< `.___\_<|>_/___.' >'"".  
               | | : `- \`.;`\ _ /`;.`/ - ` : | |  
                 \ \ `-. \_ __\ /__ _/ .-` / /  
         ======`-.____`-.___\_____/___.-`____.-'======  
                            `=---='  
  
         .............................................  
                  佛祖镇楼                  BUG辟易  
          佛曰:  
                  写字楼里写字间，写字间里程序员；  
                  程序人员写程序，又拿程序换酒钱。  
                  酒醒只在网上坐，酒醉还来网下眠；  
                  酒醉酒醒日复日，网上网下年复年。  
                  但愿老死电脑间，不愿鞠躬老板前；  
                  奔驰宝马贵者趣，公交自行程序员。  
                  别人笑我忒疯癫，我笑自己命太贱；  
                  不见满街漂亮妹，哪个归得程序员？ 
'''
# @File  : check_seat.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-11-28 - 21:51
# @Desc  : 查座位
import re

from Maoyan.downloader import Downloader
from urllib import request
from fake_useragent import UserAgent

url = 'http://maoyan.com/xseats/201811280308257?movieId=1207271&cinemaId=2548'
Downloader = Downloader()

# respronse = Downloader.get_response(url)
req = request.Request(url)
req.add_header('User-Agent', UserAgent().random)
req.add_header('Cookie', '__mta=214684200.1541052148200.1543413115306.1543413501672.10; uuid_n_v=v1; uuid=B2F7BE10DD9B11E8AC0AE9400D7CD5223517AF16897647A0BE9BC2C598B61361; _lxsdk_cuid=166cddda395c8-0901dcfa8d4da7-36664c08-100200-166cddda396c8; _lxsdk=B2F7BE10DD9B11E8AC0AE9400D7CD5223517AF16897647A0BE9BC2C598B61361; _csrf=0df093cb7af3c767f0f8356bae03914ee86ffadd557d0865dbf78ae76f0dfcf4; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=214684200.1541052148200.1543413014000.1543413029351.8; _lxsdk_s=1675a959af2-85a-2de-138%7C%7C14')
response = request.urlopen(req,timeout=120)
pageinfo = response.read().decode().replace('\n', '')

def check_seatnum(response):
    '''
    识别每一个场次的人数，已购票的，及未购票的
    :param response: 选座购票页面的网页信息
    :return:
          all_seat_num ：当前厅全部的座位总数
          all_selected_num ：当前已经被选了的座位总数
          seat_selected  ：每一个座位信息（是否已经被购买）
    '''
    seat_req = '<div class="seats-wrapper">(.*?)<div class="side">'
    seat = str(re.findall(seat_req,pageinfo)[0]).replace(' ','')
    seat_one_req = '<spanclass="seat(.*?)"data-column-id="(.*?)"data-row-id="(.*?)"data-no=".*?"data-st="(.*?)"data-act="seat-click"'
    seat_one = re.findall(seat_one_req,seat)
    all_seat_num = 0
    all_selected_num = 0
    seat_selected = []
    for i in seat_one:
        seat_info = {}
        if i[0] == 'empty':
            continue
        elif i[0] == 'sold':
            all_selected_num += 1
            all_seat_num += 1
        else:
            all_seat_num += 1
        seat_info['row_num'] = i[2]
        seat_info['colume_num'] = i[1]
        seat_info['status'] = i[-1]
        seat_selected.append(seat_info)

    return (all_seat_num, all_selected_num, seat_selected)

for i in check_seatnum(pageinfo):
    print(i)