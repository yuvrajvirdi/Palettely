import random
from math import sqrt
from point import Point
from cluster import Cluster

class KMeans:
    
    def __init__(self, n_clusters, min_diff=1):
        self.n_clusters = n_clusters
        self.min_diff = min_diff

    def euclidean(self, p, q):
        n_dim = len(p.coordinates)
        return sqrt(sum([
            (p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)
        ]))

    def calculate_center(self, points):
        n_dim = len(points[0].coordinates)
        vals = [0.0 for i in range(n_dim)]
        for p in points:
            for i in range(n_dim):
                vals[i] += p.coordinates[i]
        coords = [(v / len(points)) for v in vals]
        return Point(coords)

    def assign_points(self, clusters, points):
        p_lists = [[] for i in range(self.n_clusters)]

        for p in points:
            smallest_distance = float('inf')

            for i in range(self.n_clusters):
                distance = self.euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            
            p_lists[idx].append(p)
        
        return p_lists

    def fit(self, points):
        clusters = [Cluster(center=p, points=[p]) for p in random.sample(points, self.n_clusters)]

        while True:

            p_lists = self.assign_points(clusters, points)
            
            diff = 0

            for i in range(self.n_clusters):
                if not p_lists[i]:
                    continue
                old = clusters[i]
                center = self.calculate_center(p_lists[i])
                new = Cluster(center, p_lists[i])
                clusters[i] = new
                diff =  max(diff, self.euclidean(old.center, new.center))

            if diff < self.min_diff:
                break
        
        return clusters