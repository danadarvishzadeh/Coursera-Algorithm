#!/usr/bin/python3


import sys
from heapq import heappop, heappush


class PriorityQueue:
    def __init__(self):
        self.H = []
        self.obsolete = set()

    def put(self, item):
        heappush(self.H, item)

    def get(self):
        self.obsolete.add(self.H[0][1])
        return heappop(self.H)[1]

    def __bool__(self):
        while self.H and self.H[0][1] in self.obsolete:
            heappop(self.H)
        return len(self.H) > 0
    
    def simple_get(self):
        return heappop(self.H)

    def clear(self):
        self.H = []

    def last(self, imp):
        if self.empty():
            return False
        return self.H[0][0] < imp



class DistPreprocessSmall:
    def __init__(self, n, adj, cost):
        self.adj = adj
        self.cost = cost
        self.n = n
        self.inf = 2 * 10**6 * n
        self.rank = [self.inf for _ in range(n)]

    def preprocess(self):
        rank = 1
        for v in range(self.n):
            self.rank[v] = rank
            rank += 1
            self.process_node(v)

    def add_edge(self, u, w, c):
        self.adj[0][u].append(w)
        self.cost[0][u].append(c)
        self.adj[1][w].append(u)
        self.cost[1][w].append(c)

    def process_node(self, v):
        rank_v = self.rank[v]
        tmp = 0
        if self.cost[0][v]:
            tmp += max(self.cost[0][v])
        for cr, ur in zip(self.cost[1][v], self.adj[1][v]):
            if rank_v > self.rank[ur]:
                continue
            limit = tmp + cr
            dist = self.pre_dij(ur, v, limit)
            for c, u in zip(self.cost[0][v], self.adj[0][v]):
                if rank_v > self.rank[u]:
                    continue
                if dist.get(u, self.inf) > c + cr:
                    self.add_edge(ur, u, c + cr)
            
    def pre_dij(self, s, v, limit):
        dist = dict()
        q = PriorityQueue()
        dist[s] = 0
        q.put((0, s))
        while q:
            u = q.get()
            if dist[u] > limit:
                break
            dist_u = dist[u]
            for c, v_ in zip(self.cost[0][u], self.adj[0][u]):
                if v_ == v:
                    continue
                dist_v_ = dist.get(v_, self.inf)
                sum_ = dist_u + c
                if dist_v_ > sum_:
                    dist[v_] = sum_
                    q.put((sum_, v_))
        return dist

    def query(self, s, t):
        dist = [dict(), dict()]
        proc = [set(), set()]
        q = [PriorityQueue(), PriorityQueue()]
        estimate = self.inf
        dist[0][s] = 0
        dist[1][t] = 0
        q[0].put((0, s))
        q[1].put((0, t))
        while q[0] or q[1]:
            if q[0]:
                u = q[0].get()
        #        print('u', u+1)
                if dist[0][u] <= estimate:
                    self.process(u, dist, q, proc, 0)
                else:
                    q[0].clear()
                if u in proc[1] and dist[0][u] + dist[1][u] < estimate:
                    estimate = dist[0][u] + dist[1][u]
                    if estimate == 3388:
                        print('answer:', 'u:', u+1)
            if q[1]:
                ur = q[1].get()
        #        print('ur', ur+1)
                if dist[1][ur] <= estimate:
                    self.process(ur, dist, q, proc, 1)
                else:
                    q[1].clear()
                if ur in proc[0] and dist[0][ur] + dist[1][ur] < estimate:
                    estimate = dist[0][ur] + dist[1][ur]
                    if estimate == 3388:
                        print('answer:', 'ur:', ur+1)
        return estimate if estimate < self.inf else -1

    def debug_string(self):
        for u in range(self.n):
            for v, c in zip(self.adj[0][u], self.cost[0][u]):
                print(u+1, v+1, c)

    def process(self, u, dist, q, proc, side):
        dist_u = dist[side][u]
        #print()
        #print('side', side)
        for v, c in zip(self.adj[side][u], self.cost[side][u]):
            #print('v', v+1)
            #print('u', u+1)
            if self.rank[v] < self.rank[u]:
            #    print('here')
                continue
            dist_v = dist[side].get(v, self.inf)
            sum_ = dist_u + c
            #if sum_ == 3081:
            #    print('answer:', 'u:', u+1, 'v:', v+1)
            #if sum_ == 3388:
            #    print('answer:', 'u:', u+1, 'v:', v+1)
            if dist_v > sum_:
                dist[side][v] = sum_
                q[side].put((sum_, v))
        proc[side].add(u)


def readl():
        return map(int, sys.stdin.readline().split())


if __name__ == '__main__':
    n,m = readl()
    adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]
    for e in range(m):
        u,v,c = readl()
        adj[0][u-1].append(v-1)
        cost[0][u-1].append(c)
        adj[1][v-1].append(u-1)
        cost[1][v-1].append(c)

    ch = DistPreprocessSmall(n, adj, cost)
    ch.preprocess()
    print("Ready")
    sys.stdout.flush()
    t, = readl()
    for i in range(t):
        s, t = readl()
        #ch.debug_string()
        #print(s, t)
        print(ch.query(s-1, t-1))
        #if s ==7:
        #    break
