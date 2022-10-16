import subprocess
import numpy as np
import os
import shutil

np.random.seed(0)
string = '0 ' * 9
string = string[:-1]

if os.path.exists('task3_results'):
	shutil.rmtree('task3_results')
os.mkdir('task3_results')
os.mkdir('task3_results/i1')
os.mkdir('task3_results/i2')

print('------------------------------------------')
print('Random policy initialized for Player 1')
print('------------------------------------------')
print()

for i1 in range(3):

	print(f'Iteration {i1+1}\n')

	f = open(f'task3_results/i1/policy1_{i1}_0.txt', 'w')

	f.write('1\n')
	with open('data/attt/states/states_file_p1.txt', 'r') as f2:
		while True:
			state = f2.readline().strip()
			if state == '':
				break
			f.write(state + ' ')
			gap = np.random.choice(np.array([i for i, char in enumerate(state) if char == '0']))
			f.write(string[:2*gap] + '1' + string[2*gap+1:] + '\n')
	f.close()

	for i in range(10):

		fname1 = f'task3_results/i1/policy2_{i1}_{i+1}.txt'
		f2name1 = f'task3_results/i1/policy1_{i1}_{i}.txt'
		subprocess.call(f'python encoder.py --policy {f2name1} --states data/attt/states/states_file_p2.txt > mdp.txt', shell=True)
		subprocess.call(f'python planner.py --mdp mdp.txt > vp.txt', shell=True)
		subprocess.call(f'python decoder.py --value-policy vp.txt --states data/attt/states/states_file_p2.txt --player-id 2 > {fname1}', shell=True)

		fname2 = f'task3_results/i1/policy1_{i1}_{i+1}.txt'
		f2name2 = f'task3_results/i1/policy2_{i1}_{i+1}.txt'
		subprocess.call(f'python encoder.py --policy {f2name2} --states data/attt/states/states_file_p1.txt > mdp.txt', shell=True)
		subprocess.call(f'python planner.py --mdp mdp.txt > vp.txt', shell=True)
		subprocess.call(f'python decoder.py --value-policy vp.txt --states data/attt/states/states_file_p1.txt --player-id 1 > {fname2}', shell=True)	

		if i == 0:
			continue

		num1 = 0
		with open(f'task3_results/i1/policy1_{i1}_{i+1}.txt', 'r') as f:
			fname1_lines = f.readlines()
		with open(f'task3_results/i1/policy1_{i1}_{i}.txt', 'r') as f:
			f2name1_lines = f.readlines()
		for j in range(len(fname1_lines)):
			if fname1_lines[j] != f2name1_lines[j]:
				num1 += 1
		print(f"Difference in policies for player 1, in iterations {i} and {i+1}: {num1}")

		num2 = 0
		with open(f'task3_results/i1/policy2_{i1}_{i+1}.txt', 'r') as f:
			fname2_lines = f.readlines()
		with open(f'task3_results/i1/policy2_{i1}_{i}.txt', 'r') as f:
			f2name2_lines = f.readlines()
		for j in range(len(fname2_lines)):
			if fname2_lines[j] != f2name2_lines[j]:
				num2 += 1
		print(f"Difference in policies for player 2, in iterations {i} and {i+1}: {num2}")

		if num1 == 0 and num2 == 0:
			print("Converged!\n")
			with open(f'task3_results/i1/policy1_{i1}_{i+1}.txt', 'r') as f:
				with open(f'task3_results/i1/policy1_{i1}_optimal.txt', 'w') as f2:
					f2.writelines(f.readlines())
			with open(f'task3_results/i1/policy2_{i1}_{i+1}.txt', 'r') as f:
				with open(f'task3_results/i1/policy2_{i1}_optimal.txt', 'w') as f2:
					f2.writelines(f.readlines())
			break

print('------------------------------------------')
print('Random policy initialized for Player 2')
print('------------------------------------------')
print()

for i2 in range(3):

	print(f'Iteration {i2+1}\n')

	f = open(f'task3_results/i2/policy2_{i2}_0.txt', 'w')

	f.write('2\n')
	with open('data/attt/states/states_file_p2.txt', 'r') as f2:
		while True:
			state = f2.readline().strip()
			if state == '':
				break
			f.write(state + ' ')
			gap = np.random.choice(np.array([i for i, char in enumerate(state) if char == '0']))
			f.write(string[:2*gap] + '1' + string[2*gap+1:] + '\n')
	f.close()

	for i in range(10):

		fname1 = f'task3_results/i2/policy1_{i2}_{i+1}.txt'
		f2name1 = f'task3_results/i2/policy2_{i2}_{i}.txt'
		subprocess.call(f'python encoder.py --policy {f2name1} --states data/attt/states/states_file_p1.txt > mdp.txt', shell=True)
		subprocess.call(f'python planner.py --mdp mdp.txt > vp.txt', shell=True)
		subprocess.call(f'python decoder.py --value-policy vp.txt --states data/attt/states/states_file_p1.txt --player-id 1 > {fname1}', shell=True)

		fname2 = f'task3_results/i2/policy2_{i2}_{i+1}.txt'
		f2name2 = f'task3_results/i2/policy1_{i2}_{i+1}.txt'
		subprocess.call(f'python encoder.py --policy {f2name2} --states data/attt/states/states_file_p2.txt > mdp.txt', shell=True)
		subprocess.call(f'python planner.py --mdp mdp.txt > vp.txt', shell=True)
		subprocess.call(f'python decoder.py --value-policy vp.txt --states data/attt/states/states_file_p2.txt --player-id 2 > {fname2}', shell=True)	

		if i == 0:
			continue

		num1 = 0
		with open(f'task3_results/i2/policy1_{i2}_{i+1}.txt', 'r') as f:
			fname1_lines = f.readlines()
		with open(f'task3_results/i2/policy1_{i2}_{i}.txt', 'r') as f:
			f2name1_lines = f.readlines()
		for j in range(len(fname1_lines)):
			if fname1_lines[j] != f2name1_lines[j]:
				num1 += 1
		print(f"Difference in policies for player 1, in iterations {i} and {i+1}: {num1}")

		num2 = 0
		with open(f'task3_results/i2/policy2_{i2}_{i+1}.txt', 'r') as f:
			fname2_lines = f.readlines()
		with open(f'task3_results/i2/policy2_{i2}_{i}.txt', 'r') as f:
			f2name2_lines = f.readlines()
		for j in range(len(fname2_lines)):
			if fname2_lines[j] != f2name2_lines[j]:
				num2 += 1
		print(f"Difference in policies for player 2, in iterations {i} and {i+1}: {num2}")

		if num1 == 0 and num2 == 0:
			print("Converged!\n")
			with open(f'task3_results/i2/policy1_{i2}_{i+1}.txt', 'r') as f:
				with open(f'task3_results/i2/policy1_{i2}_optimal.txt', 'w') as f2:
					f2.writelines(f.readlines())
			with open(f'task3_results/i2/policy2_{i2}_{i+1}.txt', 'r') as f:
				with open(f'task3_results/i2/policy2_{i2}_optimal.txt', 'w') as f2:
					f2.writelines(f.readlines())
			break

os.remove('mdp.txt')
os.remove('vp.txt')