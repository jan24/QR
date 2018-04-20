#coding=utf-8
import re
import time, os, sys
import winsound #播放音乐
import db_orm
#主程序

soundFile_dict = { 'new':os.path.dirname(os.path.abspath(__file__)) + "\\audio\\railway.wav", 
'old':os.path.dirname(os.path.abspath(__file__)) + "\\audio\\wolf.wav",
 'bad':os.path.dirname(os.path.abspath(__file__)) + "\\audio\\horse.wav" } 

def playmusic(status):
    if status in ['new','old','bad']:
        winsound.PlaySound(soundFile_dict.get(status), winsound.SND_ASYNC)




#启动扫码程序，监控输入
def scan():
    #设置生产线、班次
    while True:
        a = input('请输入生产线名，数字，如总五车间输入 5\n    ')        
        m = re.fullmatch(r'\s*[1-9]|(1[0-2])\s*',a)
        if m:
            print('>>>>已设置为 总 %s 车间  ' % int(a.strip()) )
            break
        else:
            print('输入无效，请重新输入')

    b = input('请输入班次，数字，白班 1，晚班 2，中班 3，无输入则按照当前时间自动选择\n    ')
    m = re.fullmatch(r'\s*[123]\s*',b)
    if m:
        b = b.strip()
    else:
        print('输入无效')
        b=time.strftime("%H:%M", time.localtime())
        if 8 <= int(b[0:2]) <= 18: #白班 7:30——19:15
            b = '1' 
        elif b==7 and int(b[3:5])>=30:
            b = '1'
        elif b==19 and int(b[3:5])<=15:
            b = '1'
        else:
            b = '2' #晚班
    print('>>>>已按当前时间设置为 %s  \n' % {'1':'白班','2':'晚班','3':'中班'}[b] )

    SHIFT = time.strftime("%Y-%m-%d", time.localtime()) + '-'+ a.strip() +'-'+ b #形如'2017-12-15-5-1'
    print(SHIFT)

    pattern = r'\d{3}\w\d\w{2}\d{8}$' #条码格式校对 形如 368 A 7N 8 198 00127、368 A 7N Y 198 00127
    pattern = r'[a-z]\w{1,20}' #调试用

    print('>>>>开始扫码......')
    while True:
        s = str(sys.stdin.readline()).strip("\n")
        m = re.fullmatch(pattern, s)
        if m:            
            if db_orm.query_bar_isnew(s): 
                db_orm.insert(s, SHIFT)
                playmusic('new')
                print('playmusic new  该批次采集数：%s  当班产量：%s' % (db_orm.batch_count(s[4:10], SHIFT), db_orm.shift_count(SHIFT)))
            else:
                db_orm.insert(s, SHIFT,isnew=0)
                playmusic('old')
                print('playmusic old  该批次采集数：%s  当班产量：%s' % (db_orm.batch_count(s[4:10], SHIFT), db_orm.shift_count(SHIFT)))
        else:
            playmusic('bad')
            print('playmusic bad')          

    
if __name__ == '__main__':
        scan()