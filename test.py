from random import sample

total_cells = 30 * 16
mine_count = 99

x = set(sample(range(total_cells),mine_count))
y = set(range(total_cells))

a = [True,True]

print(sum(a))
