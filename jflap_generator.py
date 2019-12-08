inputs=(1,2)
outputs=(4,5,6)
nodes=(1,2,3,4,5,6)

def func(state):

        if state == 4:
            print("Ausgabe ohne Wechselgeld")
            return
        if state == 5:
            print("Ausgabe 1€ Wechselgeld")
            return
        if state == 6:
            print("Ausgabe 2€ Wechselgeld")
            return

        else:
            for inp in inputs:
                print("state {} plus {} goes to {}".format(state, inp, state+inp))
                func(state+inp)
for no in nodes:
    func(no)
    print("\n")

#Let V = ({0E,1E,2E,3E,4E,5E}, {M1,M2,RST}, {ART,R1,R2,CANCEL}, δ, ω, 0E})