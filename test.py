from engine import InferenceEngine

def forward_test(engine,universe):

    print("--"*6+"Forward Test"+"--"*6)
    print("Old universe: ", universe)
    engine.infer(universe)
    print("New universe: ", sorted(universe))

def backward_test(engine,universe,statement):
    print("--"*6+"Backward Test"+"--"*6)
    originalUniverse = universe[:]
    print("Old universe: ", universe)
    if engine.prove(statement,universe):
        print("{0} proved given {1}".format(statement,originalUniverse))
    else:
        print("can't be proved {0} given {1}".format(statement,originalUniverse))
    print("New universe: ", sorted(universe))

def main():

    print("\nBase test\n")
    with open("baseRules.rls") as rule_set:
        engine = InferenceEngine(rule_set)

        forward_test(engine,["a","b","c","e"])
        backward_test(engine,["a","b","c","e"],"z")

    print("\nAnimal rules test\n")
    with open("animalRules.rls") as rule_set:
        engine = InferenceEngine(rule_set)

        forward_test(engine,["croaks","eatsFlies"])
        backward_test(engine,["croaks","eatsFlies"],"green")



main()
