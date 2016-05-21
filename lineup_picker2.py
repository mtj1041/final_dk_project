import scraper

positions = scraper.todaysList()
pg, sg, sf, pf, c = positions['point-guards'], positions['shooting-guards'], positions['small-forwards'], positions['power-forwards'], positions['centers']

sorthelp = lambda x: x[2]

forwards = sorted(pf + sf, key=sorthelp)
guards = sorted(pg + sg, key=sorthelp)
utility = sorted(pg + sg + pf + sf + c, key=sorthelp)

def findLineup():
        bestscore = 100
        best = []
        bestscore = 0

        for point_guard in pg:
                print(point_guard)
                cost = point_guard[1]
                pp_est = point_guard[2]
                lineup = [point_guard[0]]

                for shooting_guard in sg:
                        if cost + shooting_guard[1]> 50000:
                                continue
                        cost += shooting_guard[1]
                        pp_est += shooting_guard[2]
                        lineup += [shooting_guard[0]]

                        for small_forward in sf:
                                if cost + small_forward[1]> 50000:
                                        continue
                                cost += small_forward[1]
                                pp_est += small_forward[2]
                                lineup += [small_forward[0]]

                                for power_forward in pf:
                                        if cost + power_forward[1]> 50000:
                                                continue
                                        cost += power_forward[1]
                                        pp_est += power_forward[2]
                                        lineup += [power_forward[0]]

                                        for center in c:
                                                if cost + center[1]> 50000:
                                                        continue
                                                cost += center[1]
                                                pp_est += center[2]
                                                lineup += [center[0]]
                                                
                                                for f in forwards:
                                                        if (cost + f[1] > 50000) or (f[0] in lineup):
                                                                continue
                                                        cost += f[1]
                                                        pp_est += f[2]
                                                        lineup += [f[0]]

                                                
                                                        for g in guards:
                                                                if (cost + g[1] > 50000) or (g[0] in lineup):
                                                                        continue
                                                                cost += g[1]
                                                                pp_est += g[2]
                                                                lineup += [g[0]]

                                                                for u in utility:
                                                                        if (cost + u[1] > 50000) or (u[0] in lineup):
                                                                                continue
                                                                        cost += u[1]
                                                                        pp_est += u[2]
                                                                        lineup += [u[0]]

                                                                        if bestscore < pp_est:
                                                                                bestscore = pp_est
                                                                                print(bestscore)
                                                                                print(lineup)
                                                                                best = list(lineup)

                                                                        cost -= u[1]
                                                                        pp_est -= u[2]
                                                                        lineup.pop()

                                                                cost -= g[1]
                                                                pp_est -= g[2]
                                                                lineup.pop()

                                                        cost -= f[1]
                                                        pp_est -= f[2]
                                                        lineup.pop()

                                                cost -= center[1]
                                                pp_est -= center[2]
                                                lineup.pop()

                                        cost -= power_forward[1]
                                        pp_est -= power_forward[2]
                                        lineup.pop()

                                cost -= small_forward[1]
                                pp_est -= small_forward[2]
                                lineup.pop()

                        cost -= shooting_guard[1]
                        pp_est -= shooting_guard[2]
                        lineup.pop()

        print(bestscore)
        return best
print(findLineup())
