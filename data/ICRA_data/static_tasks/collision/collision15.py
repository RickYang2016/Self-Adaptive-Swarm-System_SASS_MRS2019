all_col = 0
for k in range(15):
	with open('%d.log' % (k+1)) as f:
		lines = f.readlines()

		last = -1
		col = 0
		final = int(lines[-1])
		for line in lines:
			i = int(line)
			if i == last and i != final:
				col = col + 1
			else:
				last = i
				continue

	all_col = all_col + col
print("Collision: %d" % all_col)
