import pandas as pd
from flask import Flask, jsonify
from haversine import haversine
from shapely.geometry import LineString
from models import fetch_ais_data

def filter_large_distances(group):
    group = group.sort_values(by='create_time').reset_index(drop=True)
    if len(group) <= 1:
        return group

    keep_indices = [0]
    for i in range(1, len(group)):
        lon1, lat1 = group.loc[keep_indices[-1], ['lon', 'lat']]
        lon2, lat2 = group.loc[i, ['lon', 'lat']]
        distance = haversine((lat1, lon1), (lat2, lon2))

        # 输出调试信息
        #print(f"Point {keep_indices[-1]} to point {i} distance: {distance} meters")

        if distance <= 1:  #单位km
            keep_indices.append(i)

    # 返回过滤后的点
    return group.loc[keep_indices].reset_index(drop=True)

def get_cleaned_ais_data():
    df = fetch_ais_data()
    df = df.drop_duplicates(subset=['create_time', 'mmsi'])
    df = df[(df['lon'] >= -180) & (df['lon'] <= 180)]
    df = df[(df['lat'] >= -90) & (df['lat'] <= 90)]
    df['create_time'] = pd.to_datetime(df['create_time'])
    df_sampled = df.groupby('mmsi').apply(lambda x: x.iloc[::10]).reset_index(drop=True)
    df_cleaned = df_sampled.groupby('mmsi').apply(filter_large_distances).reset_index(drop=True)
    df_cleaned = df_cleaned.sort_values(by=['mmsi', 'create_time'])

    # 打印一些信息来检查过滤结果
    print(f"原始数据点数: {len(df)}")
    print(f"采样后数据点数: {len(df_sampled)}")
    print(f"清洗后数据点数: {len(df_cleaned)}")

    # 生成轨迹
    trajectories = []
    for mmsi, group in df_cleaned.groupby('mmsi'):
        if len(group) > 1:
            line = LineString(zip(group['lon'], group['lat']))
            coordinates = list(line.coords)
            trajectories.append({
                'mmsi': mmsi,
                'trajectory': {
                    'coordinates': coordinates
                }
            })

    # 打印轨迹数据以进行调试
    #print(f"Trajectories data: {trajectories}")

    # 返回 JSON 数据
    return jsonify({
        'trajectories': trajectories
    })

