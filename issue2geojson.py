# coding=utf-8
import requests
import json
import time
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

def parse_md(file_path):
    names = []
    lngs = []
    lats = []
    prices = []
    visits = []
    wikis_link = []
    with open(file_path, 'r') as fn:
        flines = fn.readlines()
        for line in flines[2:]:
            print(line)
            strs = line.split('|')
            #temp = line.strip('\n').split(' ')[0]
            names.append(strs[0])
            lngs.append(strs[1].strip(' '))
            lats.append(strs[2].strip(' '))
            prices.append(strs[3].strip(' '))
            visits.append(strs[4].strip(' '))
            wikis_link.append(strs[5].split('(')[1].strip(')\n'))
    return names, lngs, lats, prices, visits, wikis_link




if __name__ == "__main__":
    args = build_argparser().parse_args()
    names, lngs, lats, prices, visits, wikis_link = parse_md(args.input)

    print(f'{names} "\n" {lngs} "\n" {lats} "\n" {prices} "\n" {visits} "\n" {wikis_link}')
    points_list = []
    addrs_list = []
    add_index = 0
    for i in range(len(names)):
        points_list.append(Point(float(lngs[i]), float(lats[i])))
    p_data = {'addr': names, 'prices': prices, 'visits': visits, 'wiki': wikis_link, 'geometry': points_list}
    gdf = geopandas.GeoDataFrame(p_data, crs="EPSG:4326")
    gdf.to_file(args.output, driver='GeoJSON')
