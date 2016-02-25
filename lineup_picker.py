import scraper




positions = scraper.todaysList()

pg, sg, sf, pf, c = positions['point-guards'], positions['shooting-guards'], positions['small-forwards'], positions['power-forwards'], positions['centers']