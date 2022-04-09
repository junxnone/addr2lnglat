# coding=utf-8
import requests
import json
import geopandas
from shapely.geometry import Point
from argparse import ArgumentParser

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-i",
                        "--input",
                        help="input file path",
                        required=True,
                        type=str)
    parser.add_argument("-o",
                        "--output",
                        help="output path",
                        required=False,
                        default='result.geojson',
                        type=str)
    return parser

def read_txt2list(file_path):
    wlist = []
    with open(file_path, 'r') as fn:
        flines = fn.readlines()
        for line in flines:
            temp = line.strip('\n')
            #temp = line.strip('\n').split(' ')[0]
            wlist.append(temp)
    return wlist


def getUrl(*address):
    '''
    调用地图API获取待查询地址专属url
    最高查询次数30w/天 最大并发量160/秒
    '''
    ak = "TgV2QFgm0rUs6MM5ZujGFvVUiyQUWhjD"
    if len(address) < 1:
        return None
    else:
        for add in address:   
            url = 'http://api.map.baidu.com/geocoding/v3/?address={inputAddress}&output=json&ak={myAk}'.format(inputAddress=add,myAk=ak)  
            yield url
            

def getPosition(url):
    '''返回经纬度信息'''
    res = requests.get(url)
    json_data = json.loads(res.text)
    
    if json_data['status'] == 0:
        lat = json_data['result']['location']['lat'] #纬度
        lng = json_data['result']['location']['lng'] #经度
        print(f': {lat}-{lng}')
    else:
        print("Error output!")
        return json_data['status']
    return lat,lng



if __name__ == "__main__":
    args = build_argparser().parse_args()
    addrs = read_txt2list(args.input)
    points_list = []
    for add in addrs:
        add = "上海市 " + add
        print(add)
        add_url = list(getUrl(add))[0]
        try:
            lat,lng = getPosition(add_url)
            points_list.append(Point(lng, lat))
        except Error as e:
            print(e)
    p_data = {'addr': addrs, 'geometry': points_list}
    gdf = geopandas.GeoDataFrame(p_data, crs="EPSG:4326")
    gdf.to_file(args.output, driver='GeoJSON')
