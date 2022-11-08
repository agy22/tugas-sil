import json
from forward_chaining import KnowledgeBase, InferenceEngine

def load_mineral_classification_rules():
    f = open("rule_base_classification.json")
    rulebase_dict = json.load(f)
    f.close()
    rules = rulebase_dict["rules"]
    hardness_points = rulebase_dict["continuous_vars"]["turning_points"][0]
    specific_gravity_points = rulebase_dict["continuous_vars"]["turning_points"][1]

    return rules, hardness_points, specific_gravity_points

def clean_int_float(num):
    if (int(float(num)) == float(num)):
        num = int(num)
    else:
        num = float(num)

    return num

class MineralClassificationEngine:
    def __init__(self):
        rules, hardness_points, specific_gravity_points = load_mineral_classification_rules()

        self.KBS = KnowledgeBase(rules)
        self.hardness_points = hardness_points
        self.specific_gravity_points = specific_gravity_points
        self.inferenceEngine = InferenceEngine()
    
    def get_hardness_facts(self, hardness):
        hardness = clean_int_float(hardness)
        
        hardnesses = [["hardness", str(hardness)]]

        for point in self.hardness_points:
            hardness_limit = clean_int_float(point)
            if hardness <= hardness_limit:
                hardnesses.append(["hardness", "<="+str(hardness_limit)])
            if hardness >= hardness_limit:
                hardnesses.append(["hardness", ">="+str(hardness_limit)])

        return hardnesses
    
    def get_specific_gravity_facts(self, specific_gravity):
        specific_gravity = clean_int_float(specific_gravity)
        
        specific_gravities = [["specific-gravity", str(specific_gravity)]]

        for point in self.specific_gravity_points:
            specific_gravity_limit = clean_int_float(point)
            if specific_gravity <= specific_gravity_limit:
                specific_gravities.append(["specific-gravity", "<="+str(specific_gravity_limit)])
            if specific_gravity >= specific_gravity_limit:
                specific_gravities.append(["specific-gravity", ">="+str(specific_gravity_limit)])

        return specific_gravities
    
    def make_facts_from_list(self, field, values):
        facts = [[field, val] for val in values]
        
        return facts
    
    def infer(self, initial_facts):
        learned_facts, self.KBS = self.inferenceEngine.forward_chaining(initial_facts, self.KBS)

        return list(set(learned_facts))


r, _, _ = load_mineral_classification_rules()
KBS = KnowledgeBase(r)
inferenceEngine = InferenceEngine()
initial_facts = [["color", "white"], ["streak", "white"], ["luster", "vitreous"], ["hardness", "2"], ["specific-gravity", "2.3"], ["crystal-system", "monoclinic"], ["cleavage", "perfect"], ["diaphaneity", "translucent"], ["fracture", "conchoidal"], ["tenacity", "inelastic"]]
initial_facts = [['rock-group', 'sedimentary'], ['color', 'white'], ['streak', 'white'], ['hardness', '2'], ['specific-gravity', '2.3'], ['luster', 'vitreous'], ['fracture', 'conchoidal'], ['crystal-system', 'monoclinic'], ['cleavage', 'perfect'], ['diaphaneity', 'translucent'], ['tenacity', 'inelastic'], ['weathered', 'false'], ['magnetic', 'false']]
learned_facts, KBS = inferenceEngine.forward_chaining(initial_facts, KBS)

print(list(set(learned_facts)))