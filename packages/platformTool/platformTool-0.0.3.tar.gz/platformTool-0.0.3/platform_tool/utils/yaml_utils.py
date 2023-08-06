#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/9/23 16:51
    Desc  :     yaml工具
--------------------------------------
"""
import yaml


class YamlToDictUtils:
    """Yaml工具类"""

    def __new__(cls, *args, **kwargs):
        path = kwargs.get('filePath')
        with open(path, 'r', encoding = 'utf-8') as f:
            return yaml.load(f, Loader = yaml.FullLoader)