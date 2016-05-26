from collections import deque


q = deque(maxlen = 5)

for i in range(10):
	q.append(i)
	total = 0
	for elem in q:
		total += elem
	print total

#[u'matthew dellavedova', u'terrence ross', u'kevin durant', u'serge ibaka', u'marreese speights', u'tristan thompson', u'stephen curry', u'russell westbrook']