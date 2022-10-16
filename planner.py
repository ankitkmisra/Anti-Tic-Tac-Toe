import argparse
import numpy as np
import pulp

parser = argparse.ArgumentParser()

parser.add_argument("--mdp", help="Path to input MDP file.")
parser.add_argument("--algorithm", help="Algorithm to be used - vi, hpi, or lp.")

args = parser.parse_args()

f = open(args.mdp, 'r')

num_states = int(f.readline().strip().split()[-1])
num_actions = int(f.readline().strip().split()[-1])
end_states = [int(s) for s in f.readline().strip().split()[1:]]
end_states.sort()
if end_states == [-1]:
	end_states = []

probs = []
rews = []
for s in range(num_states):
	probs.append([dict() for i in range(num_actions)])
	rews.append([dict() for i in range(num_actions)])

line = f.readline().strip()
while line.startswith('transition'):
	trans = line.split()[1:]
	state1, action, state2, rew, prob = int(trans[0]), int(trans[1]), int(trans[2]), float(trans[3]), float(trans[4])
	probs[state1][action][state2] = prob
	rews[state1][action][state2] = rew
	line = f.readline().strip()

mdptype = line.split()[-1]
gamma = float(f.readline().strip().split()[-1])

f.close()

V = None
policy = None

if args.algorithm is None:
	args.algorithm = 'hpi'


if args.algorithm == 'vi':
	V = np.zeros(num_states)
	while True:
		new_V = np.zeros(num_states)
		new_V[:] = V
		for s in range(num_states):
			if s in end_states:
				continue
			new_V[s] = max([np.sum(np.array(list(probs[s][a].values())) * (np.array(list(rews[s][a].values())) + gamma * new_V[list(probs[s][a].keys())])) for a in range(num_actions)])
		if np.max(np.abs(new_V - V)) < 1e-8:
			V = new_V
			break
		V = new_V
	policy = [np.argmax(np.array([np.sum(np.array(list(probs[s][a].values())) * (np.array(list(rews[s][a].values())) + gamma * V[list(rews[s][a].keys())])) for a in range(num_actions)])) if s not in end_states else 0 for s in range(num_states)]


elif args.algorithm == 'hpi':
	policy = np.zeros(num_states, dtype='int')
	while True:
		done = True
		coeffs = np.zeros((num_states, num_states))
		for s in range(num_states):
			if s in end_states:
				continue
			for s2, prob in probs[s][policy[s]].items():
				coeffs[s, s2] = -gamma * prob
		coeffs = coeffs + np.eye(num_states)
		ords = np.array([np.sum(np.array(list(probs[s][policy[s]].values())) * np.array(list(rews[s][policy[s]].values()))) if s not in end_states else 0 for s in range(num_states)])
		coeffs = np.delete(np.delete(coeffs, end_states, 0), end_states, 1)
		ords = np.delete(ords, end_states)
		V = list(np.linalg.solve(coeffs, ords))
		for es in end_states:
			V.insert(es, 0)
		V = np.array(V)
		for s in range(num_states):
			if s in end_states:
				continue
			Qvals = np.array([np.sum(np.array(list(probs[s][a].values())) * (np.array(list(rews[s][a].values())) + gamma * V[list(rews[s][a].keys())])) for a in range(num_actions)])
			if np.max(Qvals) - V[s] > 1e-7:
				policy[s] = np.argmax(Qvals)
				done = False
		if done:
			#print(np.sum(V))
			break


elif args.algorithm == 'lp':
	prob = pulp.LpProblem('Planning', pulp.LpMinimize)
	cont_states = [s for s in range(num_states) if s not in end_states]
	V_vars = pulp.LpVariable.dicts('V', cont_states)
	prob += pulp.lpSum(list(V_vars.values()))
	for s in cont_states:
		for a in range(num_actions):
			prob += V_vars[s] >= pulp.lpSum([probs[s][a][k] * rews[s][a][k] + (0 if k in end_states else probs[s][a][k] * gamma * V_vars[k]) for k in probs[s][a].keys()])
	prob.solve(pulp.PULP_CBC_CMD(msg=0, gapAbs=1e-8))
	V = [v.varValue for v in V_vars.values()]
	for es in end_states:
			V.insert(es, 0)
	V = np.array(V)
	#print(np.sum(V))
	policy = [np.argmax(np.array([np.sum(np.array(list(probs[s][a].values())) * (np.array(list(rews[s][a].values())) + gamma * V[list(rews[s][a].keys())])) for a in range(num_actions)])) if s not in end_states else 0 for s in range(num_states)]


for s in range(num_states):
	print('{:.6f}'.format(round(V[s], 6)), policy[s])