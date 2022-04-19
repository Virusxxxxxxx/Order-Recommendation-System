# coding = utf-8

# 基于 item 的协同过滤推荐算法实现
import json
import math
from operator import itemgetter


class ItemBasedCF:
    def __init__(self):
        # 找到相似的20部餐品，为目标用户推荐10部餐品
        self.n_sim_meal = 20
        self.n_rec_meal = 10
        self.dataset = {}

        # 用户相似度矩阵
        self.meal_sim_matrix = {}
        self.meal_popular = {}
        self.meal_count = 0

    # 处理 comment 表中的数据
    def process_data(self, data):
        for comment in data:
            user_id, meal_id, rating = comment.user_id, comment.meal_id, comment.score
            self.dataset.setdefault(user_id, {})
            self.dataset[user_id][meal_id] = rating

    # 计算餐品之间的相似度
    def calc_meal_sim(self):
        for user, meals in self.dataset.items():
            for meal in meals:
                if meal not in self.meal_popular:
                    self.meal_popular[meal] = 0
                self.meal_popular[meal] += 1

        self.meal_count = len(self.meal_popular)

        for user, meals in self.dataset.items():
            for m1 in meals:
                for m2 in meals:
                    self.meal_sim_matrix.setdefault(m1, {})
                    self.meal_sim_matrix[m1].setdefault(m2, 0)
                    if m1 == m2:
                        self.meal_sim_matrix[m1][m2] = 0
                    else:
                        self.meal_sim_matrix[m1][m2] += 1
        print("Build co-rated users matrix success!")

        # 计算餐品之间的相似性
        print("Calculating meal similarity matrix ...")
        for m1, related_meals in self.meal_sim_matrix.items():
            for m2, count in related_meals.items():
                # 注意0向量的处理，即某餐品的用户数为0
                if self.meal_popular[m1] == 0 or self.meal_popular[m2] == 0:
                    self.meal_sim_matrix[m1][m2] = 0
                else:
                    self.meal_sim_matrix[m1][m2] = count / math.sqrt(self.meal_popular[m1] * self.meal_popular[m2])
        print('Calculate meal similarity matrix success!')

    # 针对目标用户U，找到K部相似的餐品，并推荐其N部餐品
    def recommend(self, data, user_id):
        self.process_data(data)
        self.calc_meal_sim()
        K = self.n_sim_meal
        N = self.n_rec_meal
        rank = {}
        eaten_meals = self.dataset[user_id]

        for meal, rating in eaten_meals.items():
            for related_meal, w in sorted(self.meal_sim_matrix[meal].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_meal in eaten_meals:
                    continue
                rank.setdefault(related_meal, 0)
                rank[related_meal] += w * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]
