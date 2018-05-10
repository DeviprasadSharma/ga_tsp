#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def point_distance(a, b):
    """Возвращает список расстояний между двумя массивами точек"""
    return np.linalg.norm(a - b, axis=1)


def route_distance(cities):
    """Возвращает длинну маршрута"""
    points = cities[['x', 'y']]
    distances = point_distance(points, np.roll(points, 1, axis=0))
    return np.sum(distances)
