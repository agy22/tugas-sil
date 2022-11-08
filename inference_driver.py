from forward_chaining import KnowledgeBase, InferenceEngine

initial_facts = [["month", "february"], ["happy", "true"], ["researching", "true"], ["name", "alison"]]
r1 = [[["lecturing", "true"], ["marking-practicals", "true"]], [["overworked", "true"]]]
r2 = [[["month", "february"]], [["lecturing", "true"]]]
r3 = [[["month", "february"]], [["marking-practicals", "true"]]]
r4 = [[["overworked", "true"]], [["bad-mood", "true"]]]
r5 = [[["slept-badly", "true"]], [["bad-mood", "true"]]]
r5 = [[["bad-mood", "true"]], [["happy", "false"]]]
r6 = [[["lecturing", "true"]], [["researching", "false"]]]

rules = [r1, r2, r3, r4, r5, r6]

KBS = KnowledgeBase(rules)
inferenceEngine = InferenceEngine()
learned_facts, KBS = inferenceEngine.forward_chaining(initial_facts, KBS)

print(learned_facts)