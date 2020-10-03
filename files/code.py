from Time_Dic import time

# Sorting Time_Dic
time = dict(sorted(time.items(), key=lambda x: x[0]))
for s in time:
	time[s] = dict(sorted(time[s].items(), key=lambda x: int(x[0].split(".")[0]) if "." in x[0] else 111))
n = {}
for s in time:
	n[s] = []
	for f in time[s]:
		n[s].append(f)
print(n)