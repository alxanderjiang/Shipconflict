import pandas as pd
import numpy as np

import csv
import math

import datetime
import random
from sklearn.cluster import DBSCAN

##wgs-84/gcj02坐标转换函数
# 参数定义
PI=3.14159265358979323846
ee = 0.00669342162296594323
aa = 6378245.0

# 坐标转换函数群
def transform_lat(lng, lat):
    # 输入: 经度、纬度
    # 输出: 转移纬度
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * np.sqrt(np.fabs(lng))
    ret += (20.0 * np.sin(6.0 * lng * PI) + 20.0 * np.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * np.sin(lat * PI) + 40.0 * np.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * np.sin(lat / 12.0 * PI) + 320 * np.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret

def transform_lng(lng, lat):
    # 输入: 经度、纬度
    # 输出: 转移经度
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * np.sqrt(np.fabs(lng))
    ret += (20.0 * np.sin(6.0 * lng * PI) + 20.0 * np.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * np.sin(lng * PI) + 40.0 * np.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * np.sin(lng / 12.0 * PI) + 300.0 * np.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret

def wgs84_to_gcj02(lng, lat):
    # 输入: 经度、纬度
    # 输出: GCJ02坐标
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = np.sqrt(magic)
    dlat = (dlat * 180.0) / ((aa * (1 - ee)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (aa / sqrtmagic * np.cos(radlat) * PI)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]

# ECEF直角转大地坐标
def xyztoblh(x,y,z):
    # 输入: ECEF直角坐标
    # 输出: ECEF大地坐标
    # 地球参数(WGS-84)
    es2=0.00669437999013
    # 经度
    l=math.acos(x/math.sqrt(pow(x,2)+pow(y,2)))
    # 纬度迭代初值
    m1=1/math.sqrt(pow(x,2)+pow(y,2))
    m2=aa*es2
    m3=1-es2
    temp1=z/math.sqrt(pow(x,2)+pow(y,2))
    temp2=0
    # 以下为迭代求解纬度(正切值)
    while(abs(temp1-temp2)>1e-14):
        temp2=temp1
        temp1=m1*(z+m2*temp1/math.sqrt(1+m3*pow(temp1,2)))
    # 求解高程
    tb=temp1,b=math.atan(tb)
    # 卯酉圈曲率半径
    n=aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 高程
    h=math.sqrt(pow(x,2)+pow(y,2))/math.cos(b)-aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 西半球经度符号转换
    if(y<0):
        l=-l
    return [b,l,h]

# ECEF大地转直角坐标系
def blhtoxyz(b,l,h):
    # 输入: ECEF大地坐标系
    # 输出: ECEF直角坐标系
    # 地球参数(WGS-84)
    es2=0.00669437999013
    # 卯酉圈曲率半径
    n=aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 直角坐标
    x=(n+h)*math.cos(b)*math.cos(l)
    y=(n+h)*math.cos(b)*math.sin(l)
    z=(n*(1-es2)+h)*math.sin(b)
    return [x,y,z]

# ECEF直角转大地坐标(CGCS2000)
def xyztoblh_CGCS2000(x,y,z):
    # 输入: ECEF直角坐标(CGCS2000标称空间)
    # 输出: ECEF大地坐标(CGCS2000标称空间)
    # 地球参数(CGCS2000)
    es2=0.0818191910428*0.0818191910428
    # 经度
    l=math.acos(x/math.sqrt(pow(x,2)+pow(y,2)))
    # 纬度迭代初值
    m1=1/math.sqrt(pow(x,2)+pow(y,2))
    m2=aa*es2
    m3=1-es2
    temp1=z/math.sqrt(pow(x,2)+pow(y,2))
    temp2=0
    # 以下为迭代求解纬度(正切值)
    while(abs(temp1-temp2)>1e-14):
        temp2=temp1
        temp1=m1*(z+m2*temp1/math.sqrt(1+m3*pow(temp1,2)))
    # 求解高程
    tb=temp1,b=math.atan(tb)
    # 卯酉圈曲率半径
    n=aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 高程
    h=math.sqrt(pow(x,2)+pow(y,2))/math.cos(b)-aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 西半球经度符号转换
    if(y<0):
        l=-l
    return [b,l,h]

# ECEF大地转直角坐标系(CGCS2000)
def blhtoxyz(b,l,h):
    # 输入: ECEF大地坐标系(CGCS2000)
    # 输出: ECEF直角坐标系(CGCS2000)
    # 地球参数(CGCS2000)
    es2=0.0818191910428*0.0818191910428
    # 卯酉圈曲率半径
    n=aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 直角坐标
    x=(n+h)*math.cos(b)*math.cos(l)
    y=(n+h)*math.cos(b)*math.sin(l)
    z=(n*(1-es2)+h)*math.sin(b)
    return [x,y,z] 

# 大地坐标转高斯平面坐标
def blhtoGuss(b,l,l0):
    # 输入: 纬度、经度、投影带中央经线经度
    # 输出: 高斯平面坐标
    # 地球参数
    es2=0.00669437999013
    e22=0.006739496742227
    # 转高斯坐标的变换参数
    A = 1 + 3.0 / 4 * es2 + 45.0 / 63 * es2 * es2 + 175.0 / 256 * es2 * es2 * es2 
    +11025.0 / 16384 * es2 * es2 * es2 * es2 
    +43659.0 / 65536 * es2 * es2 * es2 * es2* es2
    B = 3.0 / 4 * es2 + 15.0 / 16 * es2 * es2 + 525.0 / 512 * es2 * es2 * es2 
    +2205.0 /2048 * es2 * es2 * es2 * es2 
    + 72765.0 / 65536 * es2 * es2 * es2 * es2 * es2
    C = 15.0 / 64 * es2 * es2 + 105.0 / 256 * es2 * es2 * es2 
    +2205.0 / 4096 * es2 * es2 * es2 * es2 
    +10395.0 / 16384 * es2 * es2 * es2 * es2 * es2
    D = 35.0 / 512 * es2 * es2 * es2 + 315.0 / 2048 * es2 * es2 * es2 * es2 
    +31185.0 / 131072 * es2 * es2 * es2 * es2 * es2
    E = 315.0 / 16384 * es2 * es2 * es2 * es2 
    +3645.0 / 65536 * es2 * es2 * es2 * es2 * es2
    X0 = aa * (1 - es2) * (A * b - B / 2 * math.sin(2 * b) 
    +C / 4 * math.sin(4 * b) - D / 6 * math.sin(6* b) + E / 8 * math.sin(8 * b))
    # 卯酉圈曲率半径
    n=aa/math.sqrt(1-es2*pow(math.sin(b),2))
    # 计算公式中省略简写的参量
    # 计算与中央经差
    dl=l-l0
    t=math.tan(b)
    mew=e22*math.cos(b)*math.cos(b)
    # 主计算公式
    x = X0 + n / 2 * math.sin(b) * math.cos(b) * dl * dl
    + n / 24 * math.sin(b) * pow(math.cos(b), 3) * (5 - t * t + 9 * pow(mew, 2) + 4 * pow(mew,
    4)) * pow(dl, 4)
    n / 720 * math.sin(b) * pow(math.cos(b), 5) * (61 - 58 * t * t + pow(t, 4)) * pow(dl, 6)

    y = n * math.cos(b) * dl
    + n / 6 * pow(math.cos(b), 3) * (1 - t * t + mew * mew) * dl * dl * dl
    + n / 120 * pow(math.cos(b), 5) * (5 - 18 * t * t + pow(t, 4) + 14 * mew * mew - 58 *
    mew * mew * t * t) * pow(dl, 5)
    return [x,y]

# 高斯转大地坐标
def Gusstoblh(x,y,l0):
    # 输入: 高斯坐标, 投影带中央经线经度
    # 输出: 大地坐标
    # 地球参数
    es2=0.00669437999013
    e22=0.006739496742227
    pi=3.1415926535897932384626433832795
    # 高斯转大地坐标的变换参数
    A = 1 + 3.0 / 4 * es2 + 45.0 / 63 * es2 * es2 + 175.0 / 256 * es2 * es2 * es2 
    +11025.0 / 16384 * es2 * es2 * es2 * es2 
    + 43659.0 / 65536 * es2 * es2 * es2 * es2 *es2
    B = 3.0 / 4 * es2 + 15.0 / 16 * es2 * es2 
    +525.0 / 512 * es2 * es2 * es2 + 2205.0 /2048 * es2 * es2 * es2 * es2 
    +72765.0 / 65536 * es2 * es2 * es2 * es2 * es2
    C = 15.0 / 64 * es2 * es2 + 105.0 / 256 * es2 * es2 * es2 
    + 2205.0 / 4096 * es2 * es2* es2 * es2 
    + 10395.0 / 16384 * es2 * es2 * es2 * es2 * es2
    D = 35.0 / 512 * es2 * es2 * es2 + 315.0 / 2048 * es2 * es2 * es2 * es2 
    + 31185.0 /131072 * es2 * es2 * es2 * es2 * es2
    E = 315.0 / 16384 * es2 * es2 * es2 * es2 
    + 3645.0 / 65536 * es2 * es2 * es2 * es2 *es2
    # 迭代求解
    temp1=x/(aa*A*(1-es2))
    temp2=0
    while(abs(temp1-temp2)>0.0001/3600.0/180*pi):
        temp2=temp1
        temp1 = x / (aa * A * (1 - es2)) 
        + (B / 2 * math.sin(2 * temp1) 
        - C / 4 * math.sin(4 *temp1) 
        + D / 6 * math.sin(6 * temp1) 
        - E / 8 * math.sin(8 * temp1)) / A
    Bf=temp1
    # 计算公式参数
    n = aa / math.sqrt(1 - es2 * pow(math.sin(Bf), 2))
    m = aa * (1 - es2) / math.sqrt(pow(1 - es2 * pow(math.sin(Bf), 2), 3))
    t = math.tan(Bf)
    mew = e22 * math.cos(Bf) * math.cos(Bf)
    # 主计算公式
    b = Bf - y * y * t / 2 / m / n* (1 - y * y / 12 / n / n * (5 + mew * mew + 3 * t * t - 9 * mew * mew * t * t)
    + pow(y, 4) * (61 + 90 * t * t + 45 * t * t * t * t) / 360 / n / n / n / n)
    l = l0 + y / n / math.cos(Bf)* (1 - y * y / 6 / n / n * (1 + mew * mew + 2 * t * t)
    + pow(y, 4) / 120 / pow(n, 4) * (5 + 6 * mew * mew + 28 * t * t + 8 * mew *mew * t * t + 24 * t * t * t * t))
    return [b,l]

##时间转换函数群
# 通用时字典构造函数
def COMMTIME(year,month,day,hour,minute,second):
    Ct={"year":year,
        "month":month,
        "day":day,
        "hour":hour,
        "minute":minute,
        "second":second}
    return Ct

# 闰年判断
def isYear(year):
    # 输入: 待判断的年份
    # 返回: 是否闰年的bool变量
    if((year%4==0 and year%100!=0) or year%400==0):
        return True
    else:
        return False

# UNIX时转UTC
def time2epoch(unix_timestamp):
    # 输入: UNIX时间戳
    # 输出: 通用时间系统(年月日)时间(字符串)
    # 将Unix时间戳转换为datetime对象
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    # 将datetime对象转换为UTC时间
    utc_time = dt.astimezone(datetime.timezone.utc)

    return str(utc_time)[:-6]

def time2COMMONTIME(UNIXtime):
    # 输入: UNIX时间戳
    # 输出: 通用时间系统(年月日)时间(字符串)
    Days=int(UNIXtime)/86400
    sec=UNIXtime-Days*86400
    mday=[31,28,31,30,31,30,31,31,30,31,30,31,
          31,28,31,30,31,30,31,31,30,31,30,31,
          31,29,31,30,31,30,31,31,30,31,30,31,
          31,28,31,30,31,30,31,31,30,31,30,31 ]
    d=Days%1461
    for mon in range(0,48):
        if(d>=mday[mon]):
            d-=mday[mon]
        else:
            break
    year=1970+Days/1461*4+mon/12
    month=mon%12+1
    day=d+1
    hour=sec/3600
    minute=(sec-hour*3600)/60
    second=sec-hour*3600-minute*60

    comtime=COMMTIME(year,month,day,hour,minute,second)
    return comtime


# UTC转UNIX
def epoch2time(epoch):
    # 输入: 通用时字典
    # 输出: UNIX时间戳
    year=epoch["year"]
    month=epoch["month"]
    day=epoch["day"]
    hour=epoch["hour"]
    minute=epoch["minute"]
    second=epoch["second"]
    # 通用时距起点经过的Days
    Days=0
    for i in range(1970,year+1):
        # 整年数
        if(i!=year):
            Days+=365
            if(isYear(i)):
                Days+=1
        # 不整年数
        else:
            for j in range(1,month):
                # 大月
                if(j==1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12):
                    Days+=31
                if(j==4 or j==6 or j==9 or j==11):
                    Days+=30
                if(j==2 and isYear(year)):
                    Days+=29
                if(j==2 and (not isYear(year))):
                    Days+=28
                Days+=day
                Days-=1 #减去最后一天
        # 计算UNIX时间戳
        unixtime=Days*86400
        unixtime+=hour*3600
        unixtime+=minute*60
        unixtime+=second
        return unixtime

# GPS时转UNIX时
def gpst2time(week,second):
    # 输入: GPS周, GPS秒
    # 输出: 计算机UNIX时
    unixtime=second
    unixtime+=86400*7*week+second+315964800
    return unixtime

# UNIX时转GPS时
def time2gpst(unixtime):
    # 输入: UNIX时间
    # 输出: GPS周, GPS秒
    sec=unixtime-315964800
    week=int(sec/(86400*7))
    second=sec-week*86400*7
    return week,second

## csv数据读取函数群
def Process1(file):
    # 输入: 文件名
    # 输出: AIS数据字典 
    AIS=pd.read_csv(file)
    return AIS
## csv数据读取
def csvread(filename):
    # 输入: 待读取的文件名
    # 输出: AIS数据字典
    with open(filename, newline='') as csvfile:
        # 定义CSV阅读器
        csvreader = csv.reader(csvfile)
        # 定义行数
        count=0
        # 定义列标
        namelist=[]
        # 定义结果字典
        AIS={}
        # 定义结果列表
        timestamp=[]
        MMSI=[]
        Lon=[]
        Lat=[]
        Cog=[]
        Sog=[]
        shiptype=[]
        length=[]
        width=[]
        # 循环读取数据
        for row in csvreader:
            count+=1
            # 第一行创建字符串列表
            if(count==1):
                namelist.append(row[0])
                namelist.append(row[1])
                namelist.append(row[2])
                namelist.append(row[3])
                namelist.append(row[4])
                namelist.append(row[5])
                namelist.append(row[6])
                namelist.append(row[7])
                namelist.append(row[8])
            # 第二行开始创建数据列表
            else:
                timestamp.append(int(row[0]))
                MMSI.append(row[1])
                Lon.append(row[2])
                Lat.append(row[3])
                Cog.append(row[4])
                Sog.append(row[5])
                shiptype.append(row[6])
                length.append(row[7])
                width.append(row[8])
        # 结果字典
        AIS[namelist[0]]=timestamp 
        AIS[namelist[1]]=MMSI 
        AIS[namelist[2]]=Lon 
        AIS[namelist[3]]=Lat 
        AIS[namelist[4]]=Cog 
        AIS[namelist[5]]=Sog 
        AIS[namelist[6]]=shiptype 
        AIS[namelist[7]]=length 
        AIS[namelist[8]]=width
        return AIS

## 大圆距离计算
def distance(lon1,lon2,lat1,lat2):
    # 输入: 本船经度、他船经度、本船纬度、他船纬度
    # 输出: 大圆距离(非高斯平面距离)
    pi=np.pi
    l1=lon1*pi/180
    l2=lon2*pi/180
    a1=lat1*pi/180
    a2=lat2*pi/180
    dl=(l2-l1)/2
    da=(a2-a1)/2
    return 2*6371393*np.arcsin(np.sqrt(np.sin(da)*np.sin(da)+np.cos(a1)*np.cos(a2)*np.sin(dl)*np.sin(dl)))  

#以距离为唯一度量的冲突侦测
def process2(AIS):
    # 输入: AIS字典
    # 输出: 冲突概率、高风险船舶对、以风险逆序排序结果
    goallon=np.array(AIS.Lon[AIS.Sog>1.0])
    goallat=np.array(AIS.Lat[AIS.Sog>1.0])
    MMSI=np.array(AIS.MMSI[AIS.Sog>1.0])
    Cog=np.array(AIS.Cog[AIS.Sog>1.0])
    result=[]
    for i in range(len(goallon)):
        tlon=goallon[i]
        tlat=goallat[i]
        min=1e7
        for pos in range(len(goallon)):
            if goallon[pos]==tlon and goallat[pos]==tlat:
                continue
            dbl=distance(tlon,goallon[pos],tlat,goallat[pos])
            if dbl<min:
                min=dbl
        result.append(min)
    index_array = [i[0] for i in sorted(enumerate(result), key=lambda x:x[1])]
    heavilydanger=[]
    clambda=np.zeros(len(goallon))
    for i in range(len(goallon)):
        if goallon[i]>=121.85 and goallon[i]<=122.3 and goallat[i]>=29.7 and goallat[i]<=30.01:
            if result[i]<=500:
                heavilydanger.append(i)
        clambda[i]=1-(index_array.index(i)+1)/len(goallon)-0.4

    return clambda,heavilydanger,index_array

# 船间冲突定义与判断
def conflict_check(ship1,ship2):
    # 输入: A船船舶字典结构、B船船舶字典结构
    # 输出: 1为有冲突关系、0为无冲突关系 
    lng1=ship1['lng']
    lng2=ship2['lng']
    lat1=ship1['lat']
    lat2=ship2['lat']
    RLA=6*ship1['length']
    RSA=1.6*ship1['width']
    RLB=6*ship2['length']
    RSB=1.6*ship2['width']
    CogA=ship1['cog']/180.0*np.pi
    CogB=ship2['cog']/180.0*np.pi
    betaAB=np.arctan2(lng2-lng1,lat2-lat1)
    betaBA=np.arctan2(lng1-lng2,lat1-lat2)
    dist=distance(lng1,lng2,lat1,lat2)#两船距离
    distA=np.sqrt( (1+np.tan(betaAB-CogA)*np.tan(betaAB-CogA))/(1.0/RLA/RLA+np.tan(betaAB-CogA)*np.tan(betaAB-CogA)/RSA/RSA) )
    distB=np.sqrt( (1+np.tan(betaBA-CogB)*np.tan(betaBA-CogB))/(1.0/RLB/RLB+np.tan(betaBA-CogB)*np.tan(betaBA-CogB)/RSB/RSB) )
    if(dist<distA+distB):
        return 1
    else:
        return 0

# 将pandas格式的AIS数据转移到ships字典数组中，即域内船舶对象
def getships(AIS):
    # 输入: AIS数据字典
    # 输出: 域内船舶对象(字典数组)
    # 定义对象列表
    ships=[]
    # 提取数据列表
    goallon=np.array(AIS.Lon[AIS.Sog>1.0])
    goallat=np.array(AIS.Lat[AIS.Sog>1.0])
    MMSI=np.array(AIS.MMSI[AIS.Sog>1.0])
    Cog=np.array(AIS.Cog[AIS.Sog>1.0])
    Sog=np.array(AIS.Sog[AIS.Sog>1.0])
    sLength=np.array(AIS.length[AIS.Sog>1.0])
    sWidth=np.array(AIS.width[AIS.Sog>1.0])
    # 循环创建船舶对象
    for i in range(len(goallon)):
        tship={'lng':goallon[i],'lat':goallat[i],'MMSI':MMSI[i],
               'length':sLength[i],'width':sWidth[i],'cog':Cog[i],'sog':Sog[i]}
        # 添加到船舶对象列表
        ships.append(tship)
    return ships

# 预测船位推算
def predictpos(ship,premin):
    # 输入: 单船船舶对象, 轨迹预测时长
    # 标称航速与国际标准单位转换
    Sog=ship['sog']/60#单位换算为m/s
    # 标称航向与国际标准单位换算
    Cog=ship['cog']*np.pi/180.0#单位换算为rad
    # 提取单船对象属性
    lng=ship['lng']
    lat=ship['lat']
    # 船位预测
    S=Sog*premin
    nlat=lat+S*np.cos(Cog)/60.0
    nlng=lng+S*np.sin(Cog)/(np.cos(np.mean([lat,nlat])*np.pi/180.0))/60.0
    # 预测船位对象创建
    tship={'lng':ship['lng'],'lat':ship['lat'],'MMSI':ship['MMSI'],
               'length':ship['length'],'width':ship['width'],'cog':ship['cog'],'sog':ship['sog']}
    tship['lng']=nlng
    tship['lat']=nlat
    return tship

# 冲突概率矩阵构建
def posibilities(counts):
    # 输入: 冲突连接关系矩阵
    # 输出: 冲突概率计算值
    posb=np.zeros((counts.shape[0],counts.shape[0]))
    for i in range(counts.shape[0]):
        for j in range(counts.shape[0]):
            if i==j:
                continue
            if(np.sum(counts[i][j][0:5])):
                posb[i][j]=0.6*np.e**(0.1*np.sum(counts[i][j][0:5]))
            elif(np.sum(counts[i][j][5:10])):
                posb[i][j]=4.0/15*np.e**(0.1*np.sum(counts[i][j][5:10]))
            elif(np.sum(counts[i][j][10:15])):
                posb[i][j]=2.0/15*np.e**(0.1*np.sum(counts[i][j][10:15]))
    return posb

# 冲突概率，返回值：冲突单位矩阵，冲突概率矩阵，冲突概率列表，冲突概率倒序索引
def conflict_process(ships):
    # 输入: 域内船舶对象数组
    # 输出: 冲突连接矩阵, 冲突概率矩阵, 最大池化概率矩阵, 最大池化概率逆序排序结果
    # 冲突单位矩阵
    count=np.zeros((len(ships),len(ships),15))
    for pretime in range(0,15):
        nships=[]
        for i in range(len(ships)):
            nships.append(predictpos(ships[i],pretime))
        for i in range(len(nships)-1):
            for j in range(i+1,len(nships)):
                if(conflict_check(nships[i],nships[j])):
                    count[i][j][pretime]=1
                    count[j][i][pretime]=1
                    print(i,j,nships[i]['MMSI'],nships[j]['MMSI'],pretime)
    # 冲突概率矩阵
    posb=posibilities(count)
    # 冲突概率列表(最大池化概率) 
    posbmax=[]
    for i in range(len(ships)):
        posbmax.append(np.max(posb[i]))
        if(np.max(posb[i])>0):
            print(i,np.max(posb[i]))
    # 最大池化概率逆序结果
    sortindex=np.argsort(-np.array(posbmax))
    return count,posb,posbmax,sortindex

# 单船位置、MMSI列表获取(全局弃用)  
def getposbships(ships):
    # 输入: 域内船舶对象数组
    # 输出: 单船位置, MMSI列表
    ships_posb=[]
    MMSI_matrics=[]
    for i in range(len(ships)):
        ship_posb=[]
        ship_posb.append(ships[i]["lng"])
        ship_posb.append(ships[i]["lat"])
        # ship_posb.append(ships[i]["MMSI"])
        ships_posb.append(ship_posb)
        MMSI_matrics.append(ships[i]["MMSI"])
    return ships_posb,MMSI_matrics

# 单 船舶对 距离度量(全局弃用)
def prove_distance(ship1,ship2,posbs,MMSI_matrics,R1=0.2,R2=0.5):
    # 输入: 船舶对对象, 冲突概率矩阵, MMSI列表, 自定义参数
    # 输出: 船舶对距离度量结果
    print(ship1[2],ship2[2])
    # 冲突概率
    index1=MMSI_matrics.index(int(ship1[2]))
    index2=MMSI_matrics.index(int(ship2[2]))
    posb=posbs[index1][index2]
    # 物理距离
    Dist=distance(ship1[0],ship2[0],ship1[1],ship2[1])
    # 融合冲突概率的距离度量模型
    if(posb<R1):
        return Dist
    elif(posb<R2 and posb>=R1):
        return Dist*(1-posb)
    else:
        return 0.0

# 全局距离度量矩阵计算
def prove_distances(ships,posb,R1=0.2,R2=0.5):
    # 输入: 域内船舶对象数组, 冲突概率矩阵, 自定义参数
    # 结果距离矩阵
    Dists=np.zeros((len(ships),len(ships)),dtype=np.float64)
    # 循环解算距离
    for i in range(len(ships)-1):
        for j in range(i+1,len(ships)):
            oDist=distance(ships[i]["lng"],ships[j]["lng"],ships[i]["lat"],ships[j]["lat"])
            # 可忽略冲突
            if(posb[i][j]<R1):
                Dists[i][j]=oDist
                Dists[j][i]=oDist
            # 可容忍冲突
            elif(posb[i][j]>=R1 and posb[i][j]<R2):
                Dists[i][j]=oDist*(1-posb[i][j])
                Dists[j][i]=oDist*(1-posb[i][j])
            # 不可容忍冲突
            else:
                Dists[i][j]=0.0
                Dists[j][i]=0.0
    #返回结果距离矩阵
    return Dists

# 函数DBSCAN中的自定义距离度量参数模板函数
def getDists(x,y,Dists):
    # 输入: 行标, 列标, 距离矩阵
    # 输出: 指定行列位置的距离
    return Dists[int(x[0])][int(y[0])]

# 改进的密度聚类DBSCAN
def get_Dbscan_Groups(len_ships,eps,min_samples,allDists):
    # 输入: 域内船舶对象数组长度, 初始聚类参数(半径), 初始聚类参数(核心点数量), 距离矩阵
    # 输出: 动态簇索引列表
    # 创建聚类模型
    model=DBSCAN(eps=eps,min_samples=min_samples,metric=lambda a,b:getDists(a,b,allDists))
    preindex=np.array(range(len_ships))
    preindex=preindex.reshape(-1,1)
    # 执行聚类活动
    pre=model.fit_predict(preindex)
    # 输出聚类结果
    print(pre)
    return pre

# 簇索引提取
def get_groups(pre):
    # 输入:聚类结果索引
    # 输出:各簇簇内船舶索引列表
    groups=[]
    for i in range(np.max(pre)+1):
        group=[]
        for j in range(len(pre)):
            if(pre[j]==i):
                group.append(j)
        groups.append(group)
    return groups

# 获取子集函数(子集元素数量>=2)
def get_subset(items):
    # 输入:全集
    # 输出:元素数量>=2的子集
    N=len(items)
    subset=[]
    for i in range(2**N):
        comb=[]
        for j in range(N):
            if((i>>j)%2):
                comb.append(items[j])
        if(len(comb)!=0 and len(comb)!=1):
            subset.append(comb)
    return subset

# Shapley值中间量计算(组合内贡献差)
def getAT(subsubset,values,rank):
    # 输入: 参与者, 参与者待测矩阵, 参与者序号
    # 输出: 组合联合贡献度
    newposb=np.zeros((len(subsubset),len(subsubset)))
    newposbmin=np.zeros( (len(subsubset),len(subsubset)) )
    for i in range(len(subsubset)):
        for j in range(len(subsubset)):
            newposb[i][j]=values[subsubset[i]][subsubset[j]]
            if(i!=rank and j!=rank):
                newposbmin[i][j]=newposb[i][j]
            else:
                newposbmin[i][j]=0
    AllAT=0
    AllATm=0
    for i in range(len(subsubset)):
        AllAT+=max(newposb[i])
        AllATm+=max(newposbmin[i])
    return AllAT-AllATm

# 简化复杂度函数:计算集合中有冲突连接的子集
def get_conflict_sub(players,values):
    # 输入: 参与者, 参与者待测矩阵
    # 输出: 非零参与者
    conflict_sub=[]
    for i in range(len(players)):
        for j in range(len(players)):
            if(values[players[i]][players[j]]>0):
                conflict_sub.append(players[i])
    return conflict_sub

# shapley值计算
def get_shapley(players,values):    
    # 输入:待计算子集,全集贡献矩阵
    # 输出:shapeley值列表
    Si={}
    # 计算有值玩家组合子集
    subset=get_conflict_sub(players,values)
    subset_used=get_subset(subset)
    # 循环1:计算每一个参与者的shapley值
    for player in players:
        S_player_i=0
        # 参与者无贡献，不参与后续计算
        if(player not in subset):
            Si[player]=S_player_i
            continue    
        subsubset=[]
        # 循环2:包含player[i]的子集subsubset
        for i in range(len(subset_used)):
            if(player in subset_used[i]):
                subsubset.append(subset_used[i])
        # 循环计算shapley值
        for i in range(len(subsubset)):
            n=len(subset)
            t=len(subsubset[i])
            At=getAT(subsubset[i],values,subsubset[i].index(player))
            S_player_i+=math.factorial(t-1)*math.factorial(n-t)/math.factorial(n)*At
        Si[player]=S_player_i
    return Si

# 群组航行风险计算,返回:群组Shapley值、群组航行风险
def get_Grouprisk(players,posb,posbmax):
    # 输入:待计算子集,全集贡献矩阵,全集贡献度列表
    # 输出:群组Shapley值,群组航行风险
    risk=0
    Si=get_shapley(players,posb)
    for player in players:
        risk+=Si[player]*posbmax[player]
    return Si,risk
def get_Grouprisk_simple(players,posb,posbmax):
    # 输入:待计算子集,全集贡献矩阵,全集贡献度列表
    # 输出:群组Shapley值,群组航行风险
    risk=0
    sumposb=0
    for player in players:
        sumposb+=posbmax[player]
    Si={}
    
    for player in players:
        if(sumposb!=0.0):
            Si[player]=posbmax[player]/sumposb
        else:
            Si[player]=0.0
    for player in players:
        risk+=Si[player]*posbmax[player]
    return Si,risk

# 获取船舶簇的AIS静态信息列表
def getgroup_Static_AIS(ships,group):
    # 输入: 域内船舶对象数组, 单簇遍历对象
    # 输出: 单船舶簇的AIS静态信息列表
    shipgroups=[]
    for i in range(len(group)):
        shipgroups.append(ships[group[i]])
    return shipgroups

# 获取船舶簇经纬度范围和mmsi列表(GCJ02坐标系)
def getarea(ships,group):
    # 输入: 域内船舶对象数组, 单簇遍历对象
    # 输出: 单簇经纬度范围, MMSI列表
    shipgroups=getgroup_Static_AIS(ships,group)
    lonmax,lonmin,latmax,latmin=-180.0,180.0,-90.0,90.0
    for i in range(len(shipgroups)):
        if(shipgroups[i]["lng"]>=lonmax):
            lonmax=shipgroups[i]["lng"]
        if(shipgroups[i]["lng"]<=lonmin):
            lonmin=shipgroups[i]["lng"]
        if(shipgroups[i]["lat"]>=latmax):
            latmax=shipgroups[i]["lat"]
        if(shipgroups[i]["lat"]<=latmin):
            latmin=shipgroups[i]["lat"]
    # 坐标转换到GCJ02
    [lonmax,latmax]=wgs84_to_gcj02(lonmax,latmax)
    [lonmin,latmin]=wgs84_to_gcj02(lonmin,latmin)
    # mmsi列表
    mmsilist=[]
    for ship in ships:
        mmsilist.append(ship["MMSI"])
    return [lonmax,lonmin,latmax,latmin],mmsilist

# DCPA, TCPA计算
def CPA(ship1,ship2):
    # 输入: 船舶对对象
    # 输出: 两船DCPA、TCPA
    PI=3.14159265358979323846
    e1=0.081819790992
    # 数据提取
    lon_o=ship1['lng']
    lat_o=ship1['lat']
    speed_o=ship1['sog']
    course_o=ship1['cog']
    lon_t=ship2['lng']
    lat_t=ship2['lat']
    speed_t=ship2['sog']
    course_t=ship2['cog']

    # 调整坐标，将航海真航向圆周法的角度转化为matlab默认的零刻度朝右的逆时针圆周法
    if (course_o >=0 and course_o <=90):
        course_o_=90-course_o
    else:
        course_o_=450-course_o
 
    if (course_t >=0 and course_t <=90):
        course_t_=90-course_t
    else:
        course_t_=450-course_t
    # 两船速度分解，以本船为原点，求目标船的相对运动方向（0刻度朝上的圆周法）
    speed_Xo=speed_o*math.cos(course_o_*PI/180.0)  #速度分解成xy轴
    speed_Yo=speed_o*math.sin(course_o_*PI/180.0)
 
    speed_Xt=speed_t*math.cos(course_t_*PI/180.0)
    speed_Yt=speed_t*math.sin(course_t_*PI/180.0)
 
    diffspeed_x=speed_Xt-speed_Xo   #x和y方向的速度差（kn）
    diffspeed_y=speed_Yt-speed_Yo

    speed_r=math.sqrt((diffspeed_x)**2+(diffspeed_y)**2);  #求相对速度（kn）
    if(speed_r==0.0):
        speed_r==0.001
    if diffspeed_x==0 and diffspeed_y>0:     #在y正半轴
        k=0
    elif diffspeed_x==0 and diffspeed_y<0:     #在y负半轴
        k=0
    else:
        k=diffspeed_y/diffspeed_x
 
    if k==0:
        if abs(lon_t-lon_o)==0:
            DCPA=0
            TCPA=60*abs(lat_t-lat_o)/speed_r*60
            b=0
        else: 
            DCPA=abs(lon_t-lon_o)*60
            TCPA=60*abs(lat_t-lat_o)/speed_r*60
            b=0
    else: 
        b=(lat_t-lat_o)-k*(lon_t-lon_o)
        DCPA=abs(b)/math.sqrt(1+k*k)*60
        Y_p=b/(k*k+1)
        X_p=-b*k/(k*k+1)
        S=math.sqrt((Y_p+lat_o-lat_t)**2+(X_p+lon_o-lon_t)**2)*60
        TCPA=60*S/speed_r
    return DCPA,TCPA

# 不确定性轨迹预测
def predictpos_rand(ship,premin):
    Sog=ship['sog']/60#单位换算为纬度一分
    Cog=ship['cog']*np.pi/180.0#单位换算为rad
    lng=ship['lng']
    lat=ship['lat']
    # S=Sog*premin
    # nlat=lat+S*np.cos(Cog)/60.0
    # nlng=lng+S*np.sin(Cog)/(np.cos(np.mean([lat,nlat])*np.pi/180.0))/60.0
    nlat=lat
    nlng=lng
    for i in range(premin):
        nlat+=Sog*np.cos(Cog+random.uniform(-1/180.0*np.pi,1/180.0*np.pi))/60.0
        nlng+=Sog*np.sin(Cog+random.uniform(-1/180.0*np.pi,1/180.0*np.pi))/(np.cos(np.mean([lat,nlat])*np.pi/180.0))/60.0
    tship={'lng':ship['lng'],'lat':ship['lat'],'MMSI':ship['MMSI'],
               'length':ship['length'],'width':ship['width'],'cog':ship['cog'],'sog':ship['sog']}
    tship['lng']=nlng
    tship['lat']=nlat
    return tship

# 不确定性冲突概率计算
def posbility_rand(ship1,ship2,premin,N):
    dist=distance(ship1['lng'],ship2['lng'],ship1['lat'],ship2['lat'])
    DCPA,TCPA=CPA(ship1,ship2)
    if(DCPA>1):
        return 0.0
    # 冲突概率
    clambda=[]
    for i in range(premin):
        count=0
        for j in range(N):
            tship1=predictpos_rand(ship1,i)
            tship2=predictpos_rand(ship2,i)
            if(conflict_check(tship1,tship2)):
                count+=1
        clambda.append(float(count)/N)
    return max(clambda)