import scraper
import statsForMatchUp



positions = scraper.todaysList()
#positions is a dictionary of {position -> array of player stats}
# where each element in the array of player stats consists of a tuple of ('name', price, projected_score)
# ex. results = {'point-guards': [('russell westbrook', 11100, 52), ('stephen curry', 10700, 47), ('kyle lowry', 8300, 37), 
#               ('kyrie irving', 8400, 37), ('shaun livingston', 3200, 19), ('cory joseph', 3100, 16), 
#               ('matthew dellavedova', 2400, 14)], 'forwards': [], 'small-forwards': [('kevin durant', 10300, 49), 
#               ('lebron james', 10500, 48), ('harrison barnes', 4300, 20), ('andre iguodala', 4200, 20), ... }
pg, sg, sf, pf, c = positions['point-guards'], positions['shooting-guards'], positions['small-forwards'], positions['power-forwards'], positions['centers']
#assign the array of tuples of player info to appropriate name

sorthelp = lambda x: x[2]

#Create the broader categories by combining appropriate positions
forwards = sorted(pf + sf, key=sorthelp)
guards = sorted(pg + sg, key=sorthelp)
utility = sorted(pg + sg + pf + sf + c, key=sorthelp)

#Given the arrays of pg, sg, sf, etc. that were created above. this function will go through 8 for loops to try all legal combinations and return the best option
#Can we improve this? Do we need to? Not sure...
def findLineup():
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
#WHY DO WE HAVE ALL THIS POPPING AND SUBTRACTING? WOULDNT IT JUST BE EASIER
#TO SAVE THE BEST SCORE AND THE BEST LINEUP AND THEN SET PP_EST AND LINEUP AND COST
#BACK TO 0? AM I MISSING SOMETHING?
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