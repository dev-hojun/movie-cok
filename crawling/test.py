import csv, os
os.chdir(r'../crawling/')
# f = open('navermovie_basic2.csv', 'r')
f = open('test.csv', 'r')

new = csv.reader(f)
for i in new:
	print(i)
print("하하호홓")