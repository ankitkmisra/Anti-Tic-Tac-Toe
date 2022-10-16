import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--value-policy", help="Path to planner output.")
parser.add_argument("--states", help="Path to own states file.")
parser.add_argument("--player-id", help="Own player ID.")

args = parser.parse_args()

print(args.player_id)

f_policy = open(args.value_policy, 'r')
f_states = open(args.states, 'r')

probs = " 0" * 9

while True:
	state = f_states.readline().strip()
	if state == '':
		break
	policy = int(f_policy.readline().strip().split()[-1])
	print(state + probs[:2*policy+1] + "1" + probs[2*policy+2:])

f_policy.close()
f_states.close()