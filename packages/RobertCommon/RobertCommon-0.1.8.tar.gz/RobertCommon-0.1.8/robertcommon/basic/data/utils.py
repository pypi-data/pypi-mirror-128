from datetime import datetime, timedelta

import bson
import pandas as pd


def chunk_list(values: list, num: int):
    for i in range(0, len(values), num):
        yield values[i: i+num]

#转换类为字典
def convert_class_to_dict(obeject_class):
    object_value = {}
    for key in dir(obeject_class):
        value = getattr(obeject_class, key)
        if not key.startswith('__') and not key.startswith('_') and not callable(value):
            object_value[key] = value
    return object_value

def generate_object_id():
    return bson.ObjectId().__str__()

#补数
def fill_specified_time_data(time_datas: dict, freq: str='min', method: str='ffill') -> dict:
    '''
     补数
    :param time_datas: {"2021-08-04 00:00:00": data_sturct}
    :param freq: ["min", "5min"]
    :param method: ["", ""]补齐方式
    :return:
    '''

    times = sorted(list(time_datas.keys()))
    time_start = datetime.strptime(times[0], '%Y-%m-%d %H:%M:%S')
    time_end = datetime.strptime(times[-1], '%Y-%m-%d %H:%M:%S')

    #获取指定格式时间段
    times_index_specified = []
    for date in pd.date_range(start=time_start, end=time_end + timedelta(days=1), freq=freq, normalize=True):  # 按分钟补齐
        time = date.to_pydatetime()
        if date >= time_start and date <= time_end:
            times_index_specified.append(time.strftime('%Y-%m-%d %H:%M:%S'))

    times_index_extra = []
    for time in times:
        if time not in times_index_specified:
            times_index_extra.append(time)

    times_index_specified.extend(times_index_extra)

    dict_value = pd.DataFrame(pd.DataFrame.from_dict(time_datas).T, index=sorted(times_index_specified)).fillna(method=method).drop(times_index_extra).T.to_dict()

    #去除空值
    for time in dict_value.keys():
        for name in list(dict_value[time].keys()):
            if name in dict_value[time].keys():
                if pd.isnull(dict_value[time][name]):
                    del dict_value[time][name]

    return dict_value



