# -*- coding: utf-8 -*-
import numpy as np
import json


# 为int和float特征分段，结果为字符串形式，明确讲出值在区间的位置
def boundary(value, boundary_list):
    level = 1
    pre = None
    now = None
    for bound in boundary_list:
        now = bound
        if value < bound:
            break
        level += 1
        pre = bound
    if pre is None:
        return f'LessThan{now}'
    if pre == now:
        return f'GreaterThan{pre}'
    return f'Between{pre}and{now}'


# 格式化生成样本的原始特征字典

def feature_dict_format(attr_id_list, attr_type_list, attr_option_value_list, is_numeric_do_categorical, numeric_do_categorical_boundary):
    sample_feature_dict = {}
    iterator_matrix = np.array([attr_id_list, attr_type_list, attr_option_value_list]).T
    for attr_id, attr_type, attr_option_value in iterator_matrix:
        if attr_type == 'Select':
            # 可能的取值的json列表 Radio时列表长度==1
            if isinstance(attr_option_value, str):
                attr_option_value_json_list = json.loads(attr_option_value)
            elif isinstance(attr_option_value, list):
                attr_option_value_json_list = attr_option_value
            else:
                raise ValueError('attr_option_value_list should be json str or list of json object')
            for one_option in attr_option_value_json_list:
                # option_name = one_option['name']
                option_id = one_option['id']
                sample_feature_dict[f'{attr_id}_{option_id}'] = 1
        if attr_type == 'Number':  # FIXME 风险！！！ 如果Number类型的attr在一条样本中出现了多次，又没有选择离散化，将会只剩余一个条
            # attr_option_value 应当是一个数值
            if is_numeric_do_categorical and attr_id in numeric_do_categorical_boundary:
                # 按照给定分段阈值离散化数字特征
                val = boundary(float(attr_option_value), numeric_do_categorical_boundary[attr_id])
                sample_feature_dict[f'{attr_id}_{val}'] = 1
            elif is_numeric_do_categorical:
                # 没给阈值则每一个值都作为离散值的一个取值
                val = int(float(attr_option_value))
                sample_feature_dict[f'{attr_id}_{val}'] = 1
            else:
                # 直接作为数字特征
                sample_feature_dict[f'{attr_id}'] = float(attr_option_value)
        if attr_type in ['Checkbox', 'Radio', 'Text']:
            # Checkbox attr_option_value 应当仅有 0 ｜ 1 ｜ -1 三种值
            # Radio attr_option_value 仅给出选中的一个标签的ID值
            # Text attr_option_value 是一串不限定范围的 string
            val = attr_option_value
            sample_feature_dict[f'{attr_id}_{val}'] = 1
    return sample_feature_dict