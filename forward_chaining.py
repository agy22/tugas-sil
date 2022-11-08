class KnowledgeBase:
    SPECIFICITY = "specificity"
    RECENCY = "recency"
    ORDER = "order"

    def __init__(self, rules):
        # assumption: LHS of rules are conjunctive (i.e. no "OR")
        # alternative: split disjunctive rules into separate conjunctive LHSs

        # assumption: no generic rules (e.g. "if lecturing X then overworked X")
        # alternative: only one subject per inference (e.g. "if lecturing true then overworked true")

        # assumption: RHS of rules are additive (i.e. no "DEL fact X")
        # alternative: for binary fields, apply negated form of fact X
        # alternative: for categorical fields, apply value None for field of fact X
        self.rules = [[list(set(tuple(r) for r in rule[0])), list(set(tuple(r) for r in rule[1]))] for rule in rules]
        self.facts = []
    
    # facts with duplicate field and conflicting value may exist?
    # def occupied_field(self, fact):
    #     return fact[0] in [f[0] for f in self.facts]

    def init_facts(self, facts):
        # assumption: facts is array of field-value pairs
        # e.g. [["color", "brown"], ["parity", "even"], ["shape", "round"]]
        #       color  = brown
        #       parity = even
        #       shape  = round

        self.facts = [tuple(f) for f in facts]
    
    def write_fact(self, fact):
        if tuple(fact) not in self.facts:
            self.facts.append(fact)
        
        # # schema for unique fields only
        # if not self.occupied_field(fact):
        #     self.facts.append(fact)
        # else:
        #     for i, f in enumerate(self.facts):
        #         if f[0] == fact[0]:
        #             del_idx = i
        #             break
        #     self.facts.pop(del_idx)
        #     self.facts.append(fact)
    
    def add_rule(self, rule):
        add_rule = [set(tuple(r_) for r_ in rule[0]), set(tuple(r_) for r_ in rule[1])]
        if set(tuple(r_) for r_ in add_rule[0]) not in [set(tuple(r_) for r_ in r[0]) for r in self.rules]:
            self.rules.append(add_rule)
    
    def evaluate_rule_application(self, valid_rules, cr_strategy):
        specificity = [0 for _ in valid_rules]
        recency = [0 for _ in valid_rules]
        order = [0 for _ in valid_rules]

        for i, rule in enumerate(valid_rules):
            specificity[i] = len(list(rule[0]))
            order[i] = len(self.rules)-self.rules.index(rule)
            
            for fact in list(rule[0]):
                # assumption: fact exist in known facts
                recency[i] += len(self.facts)-self.facts.index(fact)
        
        eval_list = [[idx, [0 for _ in cr_strategy]] for idx in range(len(valid_rules))]

        # conflict resolution strategy implementation
        for i, cr_rule in enumerate(cr_strategy):
            use_rule = None

            if cr_rule == KnowledgeBase.SPECIFICITY:
                use_rule = [_ for _ in specificity]
            elif cr_rule == KnowledgeBase.RECENCY:
                use_rule = [_ for _ in recency]
            elif cr_rule == KnowledgeBase.ORDER:
                use_rule = [_ for _ in order]
            
            if use_rule is None:
                raise ValueError('Invalid conflict resolution strategy. Valid rules are "specificity", "recency", and "order".')
            for j, val in enumerate(use_rule):
                eval_list[j][1][i] = val
            
        # multikey sort based on conflict resolution strategy
        final_idxs = [e[0] for e in sorted(eval_list, key=lambda x: [x[1][i] for i in range(len(cr_strategy))], reverse=True)]

        return valid_rules[final_idxs[0]]
    
    def match_rule(self, used_rules, cr_strategy):
        # assumption: first priority is refractoriness, to prevent infinite loops

        valid_rules = []
        for i, r in enumerate(self.rules):
            # refractoriness check
            if r not in used_rules:
                add = True

                for f in r[0]:
                    if f not in self.facts:
                        add = False
                if add:
                    valid_rules.append(r)
        
        if valid_rules == []:
            return None

        return self.evaluate_rule_application(valid_rules, cr_strategy)

class InferenceEngine:
    DEFAULT_STRATEGY = ["specificity", "recency", "order"]

    def __init__(self, cr_strategy=None):
        self.used_rules = []
        if cr_strategy is None:
            cr_strategy = InferenceEngine.DEFAULT_STRATEGY
        self.cr_strategy = cr_strategy
    
    def forward_chaining(self, initial_facts, knowledgeBase, cr_strategy=None):
        if cr_strategy is not None:
            self.cr_strategy = cr_strategy
        
        knowledgeBase.init_facts(initial_facts)
        self.used_rules = []
        learned_facts = []

        apply_rule = knowledgeBase.match_rule(self.used_rules, self.cr_strategy)

        while apply_rule is not None:
            for fact in apply_rule[1]:
                knowledgeBase.write_fact(fact)
                learned_facts.append(fact)
            self.used_rules.append(apply_rule)
            apply_rule = knowledgeBase.match_rule(self.used_rules, self.cr_strategy)
        
        return learned_facts[::-1], knowledgeBase
