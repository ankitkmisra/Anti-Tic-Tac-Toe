import argparse
import math

def won(state):
	return (state[0] == state[1] and state[1] == state[2] and state[0] != '0') or (state[3] == state[4] and state[4] == state[5] and state[3] != '0') or (state[6] == state[7] and state[7] == state[8] and state[6] != '0') or (state[0] == state[3] and state[3] == state[6] and state[0] != '0') or (state[1] == state[4] and state[4] == state[7] and state[1] != '0') or (state[2] == state[5] and state[5] == state[8] and state[2] != '0') or (state[0] == state[4] and state[4] == state[8] and state[0] != '0') or (state[2] == state[4] and state[4] == state[6] and state[2] != '0')

parser = argparse.ArgumentParser()

parser.add_argument("--policy", help="Path to adversary's policy file.")
parser.add_argument("--states", help="Path to own states file.")

args = parser.parse_args()

f_states = open(args.states, 'r')
f_policy = open(args.policy, 'r')

states_list = [x.strip() for x in f_states.readlines()]
states_dict = dict(zip(states_list, range(len(states_list))))

policy_list = [x.strip() for x in f_policy.readlines()]
player = 3-int(policy_list[0])
policy_list = [x.split() for x in policy_list[1:]]
policy_dict = dict(zip([x[0] for x in policy_list], [[float(y) for y in x[1:]] for x in policy_list]))

f_states.close()
f_policy.close()

end_state = len(states_list)

print("numStates", end_state + 1)
print("numActions 9")
print("end", end_state)
for s in states_list:
	for a in range(9):
		terminal_prob = 0
		terminal_rew = 0
		if s[a] != '0':
			#print("transition", states_dict[s], a, end_state, -1, 1.0)
			terminal_prob = 1.0
			terminal_rew = -1
		else:
			next_s = s[:a] + str(player) + s[a+1:]
			if next_s not in policy_dict.keys():
				#print("transition", states_dict[s], a, end_state, 0, 1.0)
				terminal_prob = 1.0
				terminal_rew = 0
			else:
				lst = policy_dict[next_s]
				for a2 in range(9):
					if lst[a2] != 0:
						next_next_s = next_s[:a2] + str(3-player) + next_s[a2+1:]
						if next_next_s in states_list:
							print("transition", states_dict[s], a, states_dict[next_next_s], 0, lst[a2])
						elif won(next_next_s):
							#print("transition", states_dict[s], a, end_state, 1, lst[a2])
							terminal_prob += lst[a2]
							terminal_rew += lst[a2]
						else:
							#print("transition", states_dict[s], a, end_state, 0, lst[a2])
							terminal_prob += lst[a2]
		if terminal_prob > 0:
			print("transition", states_dict[s], a, end_state, terminal_rew/terminal_prob, terminal_prob)
print("mdptype episodic")
print("discount 1")