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
def feature_dict_format(attr_id_list, attr_type_list, attr_option_value_list, is_numeric_do_categorical,
                        numeric_do_categorical_boundary):
    sample_feature_dict = {}
    iterator_matrix = np.array([attr_id_list, attr_type_list, attr_option_value_list]).T
    for attr_id, attr_type, attr_option_value in iterator_matrix:
        tmp_feature_dict = extract_one_attr(attr_id, attr_type, attr_option_value, is_numeric_do_categorical,
                                            numeric_do_categorical_boundary)
        sample_feature_dict.update(tmp_feature_dict)
    return sample_feature_dict


# 提取一个attr的值变为dict，当attr_type=='Select'时可能会有多个attrOptionsValue，返回结果中会有多个kv
def extract_one_attr(attr_id, attr_type, attr_option_value, is_numeric_do_categorical, numeric_do_categorical_boundary):
    tmp_feature_dict = {}
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
            tmp_feature_dict[f'{attr_id}_{option_id}'] = 1
    if attr_type == 'Number':  # FIXME 风险！！！ 如果Number类型的attr在一条样本中出现了多次，又没有选择离散化，将会只剩余一个条
        # attr_option_value 应当是一个数值
        if is_numeric_do_categorical and attr_id in numeric_do_categorical_boundary:
            # 按照给定分段阈值离散化数字特征
            val = boundary(float(attr_option_value), numeric_do_categorical_boundary[attr_id])
            tmp_feature_dict[f'{attr_id}_{val}'] = 1
        elif is_numeric_do_categorical:
            # 没给阈值则每一个值都作为离散值的一个取值
            val = int(float(attr_option_value))
            tmp_feature_dict[f'{attr_id}_{val}'] = 1
        else:
            # 直接作为数字特征
            tmp_feature_dict[f'{attr_id}'] = float(attr_option_value)
    if attr_type in ['Checkbox', 'Radio', 'Text']:
        # Checkbox attr_option_value 应当仅有 0 ｜ 1 ｜ -1 三种值
        # Radio attr_option_value 仅给出选中的一个标签的ID值
        # Text attr_option_value 是一串不限定范围的 string
        val = attr_option_value
        tmp_feature_dict[f'{attr_id}_{val}'] = 1
    return tmp_feature_dict


# 为每个attr_option_value标注效果：好、中、坏
# 要求 attr_option_single_value_list 中每个元素都是单值的
# attr_type=='Select' 时要将多个选项拆开，否则 raise ValueError
def mark_feature_weight_and_polarity(attr_option_single_value_list, is_numeric_do_categorical,
                                     numeric_do_categorical_boundary, feature_weight_dict):
    good_attr_list = []
    mediocre_attr_list = []
    bad_attr_list = []
    for one_attr in attr_option_single_value_list:
        tmp_attr_id = one_attr['attrId']
        tmp_attr_type = one_attr['attrType']
        tmp_attr_options_value = one_attr['attrOptionsValue']
        tmp_feature = extract_one_attr(tmp_attr_id, tmp_attr_type, tmp_attr_options_value, is_numeric_do_categorical,
                                       numeric_do_categorical_boundary)
        if len(tmp_feature) > 1:
            raise ValueError(
                'each element in attr_option_single_value_list should have exactly one attr_options_value!!!')
        for key in tmp_feature.keys():
            if key in feature_weight_dict:
                one_attr['feature_weight'] = feature_weight_dict[key]
                if float(feature_weight_dict[key]) > 0.0:
                    good_attr_list.append(one_attr)
                elif float(feature_weight_dict[key]) < 0.0:
                    bad_attr_list.append(one_attr)
                elif float(feature_weight_dict[key]) == 0.0:
                    mediocre_attr_list.append(one_attr)
    return good_attr_list, mediocre_attr_list, bad_attr_list


if __name__ == '__main__':
    numeric_do_categorical_boundary = {'59': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    feature_weight_dict = {'53_1632911866107': '0.0', '53_1632911867155': '0.2', '53_1632911867916': '0.0',
                           '53_1632911891147': '0.0', '53_1632911895187': '0.0', '53_1632911901083': '0.0',
                           '53_1632911908491': '0.0', '54_1632911959028': '0.5890415585449821',
                           '54_1632911968427': '0.0', '54_1632911998604': '0.0', '54_1632912007348': '0.0',
                           '54_1632912016700': '-3.619868585734024', '58_0': '0.0', '58_1': '1.8093818019494496',
                           '59_Between10and20': '0.0', '59_Between20and30': '0.0', '59_Between60and70': '0.0',
                           '59_Between70and80': '0.0', '59_Between80and90': '0.0', '59_LessThan10': '0.0'}
    attr_list_a = [
        {
            "name": "",
            "attrId": 53,
            "labelId": "5",
            "entityId": "1",
            "attrType": "Select",
            "attrOptions": '[{"name":"AI修复","id":1632911866107},{"name":"蓝光","id":1632911867155},{"name":"超清","id":1632911867916},{"name":"高清","id":1632911891147},{"name":"标清","id":1632911895187},{"name":"模糊","id":1632911901083},{"name":"其他","id":1632911908491}]',
            "attrOptionsValue": '[{"name":"AI修复","id":1632911866107},{"name":"蓝光","id":1632911867155}]'
        },
        {
            "name": "",
            "attrId": 54,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Radio",
            "attrOptions": "",
            "attrOptionsValue": "1632911959028"
        },
        {
            "name": "",
            "attrId": 58,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Checkbox",
            "attrOptions": "",
            "attrOptionsValue": "1"
        },
        {
            "name": "",
            "attrId": 59,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Number",
            "attrOptions": "",
            "attrOptionsValue": "10"
        },
        {
            "name": "",
            "attrId": 53,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Select",
            "attrOptions": "[]",
            "attrOptionsValue": '[{"name":"超清","id":1632911867916},{"name":"高清","id":1632911891147},{"name":"标清","id":1632911895187}]'
        },
        {
            "name": "",
            "attrId": 54,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Radio",
            "attrOptions": "[]",
            "attrOptionsValue": "1632911968427"
        },
        {
            "name": "",
            "attrId": 58,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Checkbox",
            "attrOptions": "[]",
            "attrOptionsValue": "0"
        },
        {
            "name": "",
            "attrId": 59,
            "labelId": "5",
            "entityId": "5",
            "attrType": "Number",
            "attrOptions": "[]",
            "attrOptionsValue": "27"
        }
    ]
    a, b, c = mark_feature_weight_and_polarity(attr_list_a, True, numeric_do_categorical_boundary, feature_weight_dict)
    print(f'{a}')
    print(f'{b}')
    print(f'{c}')
