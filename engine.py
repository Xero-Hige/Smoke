class Rule(object):
    """docstring for Rule"""
    def __init__(self, causes,consecuenses):
        self.causes = causes[:]
        self.consecuenses = consecuenses[:]

    def is_fullfilled(self,universe):
        for cause in self.causes:
            if not cause in universe:
                return False

        return True

    def get_causes(self):
        return self.causes[:]

    def get_consecuenses(self):
        return self.consecuenses[:]

class InferenceEngine(object):
    """docstring for InferenceEngine"""
    def __init__(self, ruleset):
        ''' '''

        self.rules = {}
        self.rules_index = {}

        self._parse_rules(ruleset)

    def _parse_rules(self,rulesFile):
        for line in rulesFile:
            if not line.rstrip():
                continue
            try:
                causes_string,consecuenses_string = line.rstrip().split("IF")[1].split("THEN")
            except Exception as e:
                raise e

            causes = [cause.replace(" ","") for cause in causes_string.split(",") if cause]
            consecuenses = [consecuence.replace(" ","") for consecuence in consecuenses_string.split(",") if consecuence]

            rule = Rule(causes,consecuenses)

            for cause in causes:
                rules_list = self.rules.get(cause,[])
                rules_list.append(rule)
                self.rules[cause] = rules_list

            for consecuence in consecuenses:
                rules_list = self.rules_index.get(consecuence,[])
                rules_list.append(rule)
                self.rules_index[consecuence] = rules_list

    def infer(self,universe):
        queue = []
        for statement in universe:
            queue.append(statement)

        while (len(queue)>0):
            statement = queue.pop(0)
            for rule in self.rules.get(statement,[]):
                if not rule.is_fullfilled(universe):
                    continue

                new_statements = rule.get_consecuenses()

                for new_statement in new_statements:
                    if new_statement in universe:
                        continue

                    print("Infered from",rule.get_causes()," -> ",new_statement)
                    self._updateUniverse(universe,new_statement)
                    queue.append(new_statement)

    def _updateUniverse(self,universe,statement):
        if statement in universe:
            return
        print("Universe updated with: ",statement)
        universe.append(statement)

    def prove(self,statement,universe):
        if statement in universe:
            return True

        if not statement in self.rules_index:
            return False

        for rule in self.rules_index[statement]:
            if rule.is_fullfilled(universe):
                self._updateUniverse(universe,statement)
                return True

        for rule in self.rules_index[statement]:
            causes = rule.get_causes()
            for cause in causes:
                if not self.prove(cause,universe):
                    break

            self._updateUniverse(universe,statement)
            return True

        return False
