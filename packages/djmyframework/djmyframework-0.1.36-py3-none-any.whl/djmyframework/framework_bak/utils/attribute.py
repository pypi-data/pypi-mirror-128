# -*- coding: utf-8 -*-
# @Time    : 2021/9/16 14:45 
# @Author  : xzr
# @File    : attribute.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


class CacheAttribute(object):
    """计算对象属性,并缓存之
    """

    def __init__(self, method, name=None):
        self.method = method
        self.__doc__ = getattr(method, '__doc__')
        self.name = name or method.__name__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst)
        setattr(inst, self.name, result)
        return result


class CachedClassAttribute(CacheAttribute):
    """计算类属性,并在类中缓存之
    """

    def __get__(self, inst, cls):
        for sub_cls in cls.__subclasses__():
            # 缓存一次所有的子类属性
            if not hasattr(sub_cls, self.name):
                super(CachedClassAttribute, self).__get__(sub_cls, sub_cls)
        return super(CachedClassAttribute, self).__get__(cls, cls)