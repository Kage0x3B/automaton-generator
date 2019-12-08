from collections import defaultdict
from lxml import etree


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


class JFFWriter():
    def __init__(self, objects):
        self.objects = objects
        self.states = list(objects.keys())
        self.file = "out.jff"
        self.ids={}
        """
        <transition>&#13;
			<from>0</from>&#13;
			<to>0</to>&#13;
			<read>q</read>&#13;
			<transout>c1</transout>&#13;
		</transition>&#13;
		
        """

    def gen_output(self):
        structure = etree.Element('structure')
        structure.append(etree.Comment('Created with JFLAP - Python'))
        tp = etree.SubElement(structure, 'type')
        tp.text="mealy"
        am = etree.SubElement(structure, 'automaton')

        #generate nodes#
        x_coord=0
        y_coord=0
        for index,state in enumerate(self.states, start=1):

            if state=="init":
                s = etree.SubElement(am, 'state')
                s.attrib['id']=str(index)
                s.attrib['name']=state
                x = etree.SubElement(s, "x")
                x.text=str(x_coord)
                y = etree.SubElement(s, "y")
                y.text = str(y_coord)
                etree.SubElement(s, "initial")
            else:
                s = etree.SubElement(am, 'state')
                s.attrib['id']=str(index)
                s.attrib['name']=state
                x = etree.SubElement(s, "x")
                x.text=str(x_coord)
                y = etree.SubElement(s, "y")
                y.text = str(y_coord)

                etree.SubElement(s, "initial")
            x_coord+=100
            y_coord+=100
            self.ids[state]=index

        print(self.ids)
        for index,state in enumerate(self.states, start=0):
            for fro, inp, to, op in self.objects[state]:
                #print(fro, inp, to, op)
                print(self.ids[fro],self.ids[to],inp,op)
            #break


        with open(self.file,"w")as f:
            f.write(etree.tostring(structure, pretty_print=True).decode("utf-8"))

if __name__ == '__main__':
    states = ['init']

    for i in range(1, 7):
        states.append(str(i))
        states.append('R' + str(i))

    inputs = ['1', '2', 'RST', 'KAUFEN', 'CLK']
    outputs = ['NICHTS', 'R1', 'R2', 'WARE']

    #Generate Output file
    automaton_generator = AutomatonGenerator(states, inputs, outputs, vending_machine_func)
    JFFWriter(automaton_generator.create_automaton()).gen_output()

