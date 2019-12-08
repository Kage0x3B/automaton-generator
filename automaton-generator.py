from collections import defaultdict


class AutomatonGenerator:
    def __init__(self, states, inputs, outputs, func):
        self.states = states
        self.inputs = inputs
        self.outputs = outputs
        self.func = func

    def create_automaton(self):
        transitions = defaultdict(list)

        for state in self.states:
            for inp in self.inputs:
                transition = vending_machine_func(state, inp)
                transitions[state].append((state, inp, transition[0], transition[1]))

                print(state, " --", inp, "-->", transition)

        return transitions


def vending_machine_func(state, inp):
    state_value = 0
    try:
        state_value = int(state)
    except ValueError:
        pass

    inp_value = -1
    try:
        inp_value = int(inp)
    except ValueError:
        pass

    if state[0] == 'R':  # Return state
        if inp == 'CLK':
            return_amount = int(state[1])

            if return_amount > 2:
                return_amount = 2

            left_over_money = int(state[1]) - return_amount

            new_state = 'R' + str(left_over_money)

            if left_over_money <= 0:
                new_state = 'init'

            return new_state, 'R' + str(return_amount)
        elif not inp_value == -1:
            return state, 'R' + inp
        else:
            return state, 'NICHTS'

    if inp == 'CLK':
        return state, 'NICHTS'
    elif inp == 'RST':
        return 'R' + str(state_value), 'NICHTS'
    elif inp == 'KAUFEN':
        if state_value < 4:
            return state, 'NICHTS'
        else:
            left_over_money = state_value - 4

            if left_over_money > 0:
                return 'R' + str(left_over_money), 'WARE'
            else:
                return 'init', 'WARE'
    else:
        inp_num = int(inp)
        out_num = state_value + inp_num

        if out_num > 6:
            diff = out_num - 6

            return '6', 'R' + str(diff)

        return str(out_num), 'NICHTS'


if __name__ == '__main__':
    states = ['init']

    for i in range(1, 7):
        states.append(str(i))
        states.append('R' + str(i))

    inputs = ['1', '2', 'RST', 'KAUFEN', 'CLK']
    outputs = ['NICHTS', 'R1', 'R2', 'WARE']

    automaton_generator = AutomatonGenerator(states, inputs, outputs, vending_machine_func)
    transitions = automaton_generator.create_automaton()
    print(transitions)
