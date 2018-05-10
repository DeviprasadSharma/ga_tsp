#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv

from distance import route_distance
from ga_solver import CGASolver
from io_helper import read_tsp


if __name__ == '__main__':
    assert len(argv) == 2, "Correct use: python3 main.py <filename>.tsp"

    tsp_map = read_tsp(argv[1])

    ga_solver = CGASolver(tsp_map)
    route = ga_solver.solve(100000)

    distance = route_distance(tsp_map.reindex(route))
    print('Route found of length {}'.format(distance))
