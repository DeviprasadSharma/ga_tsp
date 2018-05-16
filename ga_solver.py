#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from distance import point_distance
from io_helper import normalize
from plot import plot_population, plot_route


class CGASolver(object):
    def __init__(self, tsp_map):
        # Формируем нормализованный набор городов (с координатой в [0,1])
        self.__cities = tsp_map.copy()
        self.__cities[['x', 'y']] = normalize(self.__cities[['x', 'y']])

        # Увеличиваем численность популяции в 8 раз
        self.__population_size = self.__cities.shape[0] * 8

        self.__population = self.__generate_population(self.__population_size)
        print('GA population have {} elements. Starting the iterations:'.format(self.__population_size))

    def solve(self, iterations, killing_rate=0.8):
        for i in range(iterations):
            if not i % 100:
                print('\t> Iteration {}/{}'.format(i, iterations))

            city = self.__cities.sample(1)[['x', 'y']].values
            winner_idx = self.__reduction(self.__population, city)
            self.__mutation(city, winner_idx, killing_rate)
            killing_rate *= 0.99997

            if not i % 1000:
                plot_population(self.__cities, self.__population, name='diagrams/{:05d}.png'.format(i))

            # Проверка на корректность координат в TSP карте
            if self.__population_size < 1:
                print('Radius has completely decayed, finishing execution at {} iterations'.format(i))
                break
            if killing_rate < 0.001:
                print('Killing rate has completely decayed, finishing execution at {} iterations'.format(i))
                break
        else:
            print('Completed {} iterations.'.format(iterations))

        route = self.__get_route(self.__cities, self.__population)
        plot_population(self.__cities, self.__population, name='diagrams/final.png')
        plot_route(self.__cities, route, 'diagrams/route.png')
        return route

    @staticmethod
    def __generate_population(size):
        """
        Генерация популяции заданного размера.

        Возвращает вектор двумерных точек на интервале [0,1].
        """
        return np.random.rand(size, 2)

    @staticmethod
    def __neighborhood_crossover(center, radix, domain):
        """
        Операция кроссовера: формирование гауссовского диапазона заданного радиуса
        вокруг центрального индекса.
        """
        if radix < 1:
            radix = 1

        # Подсчет кругового расстояния популяции до центра
        deltas = np.absolute(center - np.arange(domain))
        distances = np.minimum(deltas, domain - deltas)

        # Расчет распределения Гаусса вокруг данного центра
        return np.exp(-(distances * distances) / (2 * (radix * radix)))

    def __mutation(self, city, winner_idx, killing_rate=0.8):
        gaussian = self.__neighborhood_crossover(winner_idx,
                                                 self.__population_size // 10,
                                                 self.__population.shape[0])
        self.__population += gaussian[:, np.newaxis] * killing_rate * (city - self.__population)
        self.__population_size = self.__population_size * 0.9997

    @staticmethod
    def __reduction(candidates, origin):
        """Операция редукции: Возвращает индекс ближайшего кандидата к данной точке"""
        return point_distance(candidates, origin).argmin()

    def __get_route(self, cities, population):
        """Возращает маршрут, рассчитанный по переданной популяции"""
        cities['winner'] = cities[['x', 'y']].apply(
            lambda c: self.__reduction(population, c),
            axis=1,
            raw=True
        )
        return cities.sort_values('winner').index
