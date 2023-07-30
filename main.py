from typing import Dict
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import folium

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.font_manager import FontProperties



_ = load_dotenv()
URL = "https://restapi.amap.com/v3/place/text?parameters"
KEY = os.getenv("GAODE_KEY")

def request_poi(params: Dict) -> Dict:
    try:
        # 发送GET请求，并将参数传递给params参数
        response = requests.get(URL, params=params)

        # 检查响应状态码
        if response.status_code == 200:
            # 请求成功
            data = response.json()  # 解析响应的JSON数据
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # 请求异常
        print("An error occurred:", e)



def get_poi_data():


    data = {
        "name": [],
        "address": [],
        "pname": [],
        "cityname": [],
        "type": [],
        "typecode": [],
        "adname": [],
        "location": [],
    }
    pages = 1000
    params = {
        "key": KEY,
        "types": "170206",
        "city": "440106",
        "citylimit": "true",
        "extensions": "all",
    }
    for i in range(pages):
        params["page"] = i
        poi_json = request_poi(params)


        # Extract data from the JSON
        for poi in poi_json["pois"]:
            data["address"].append(poi["address"])
            data["pname"].append(poi["pname"])
            data["cityname"].append(poi["cityname"])
            data["type"].append(poi["type"])
            data["typecode"].append(poi["typecode"])
            data["adname"].append(poi["adname"])
            data["name"].append(poi["name"])
            data["location"].append(poi["location"])

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel("poi_data.xlsx", index=False)

    print("Data saved to poi_data.xlsx successfully!")


# def draw():
#     # 添加中文标识
#     chinese_font_path = os.getenv("CHINESE_FONT_PATH")  # 请将路径替换为您的中文字体文件路径
#     chinese_font = FontProperties(fname=chinese_font_path)
#     #读取excel,取location这一类，将数据格式化为lons和lats
#     df = pd.read_excel("poi_data.xlsx")
#     lons = df["location"].str.split(",", expand=True)[0].astype(float)
#     lats = df["location"].str.split(",", expand=True)[1].astype(float)
#     labels = range(1, len(df["name"]))
#
#     # 创建地图
#     fig = plt.figure(figsize=(10, 6))
#     ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
#
#     # 绘制经纬度点
#     ax.scatter(lons, lats, color='red', marker='o', transform=ccrs.Geodetic())
#
#     for lat, lon, label in zip(lats, lons, labels):
#         plt.text(lon, lat, label,  fontproperties=chinese_font, fontsize=9, ha='right', va='bottom',
#                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
#
#     plt.title('Map of Points with Cartopy')
#     plt.show()


def draw_by_folium():

    # 广州天河区的经纬度
    latitude = 23.135769
    longitude = 113.339103

    # 创建地图对象，以广州天河区为中心
    m = folium.Map(location=[latitude, longitude],
                   tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
                   attr='高德-中英文对照',
                   zoom_start=13)

    # 读取csv,取location这一类，将数据格式化为lons和lats,同时将name设为label
    df = pd.read_csv("./GBK/广州市_公司企业_20220602_041919.csv", encoding='utf-8')
    df = df[(df["小类"] == "网络科技") & (df["adcode"] == 440106)]
    lons = df["location"].str.split(",", expand=True)[0].astype(float)
    lats = df["location"].str.split(",", expand=True)[1].astype(float)
    labels = df["name"]
    locations = list(zip(lats, lons, labels))

    # 在地图上添加标记和标签
    for lat, lon, label in locations:
        folium.Marker(location=[lat, lon], popup=label).add_to(m)

    # 保存地图为HTML文件
    m.save('guangzhou_map_with_labels.html')

if __name__ == '__main__':
    # get_poi_data()
    # draw()
    draw_by_folium()

