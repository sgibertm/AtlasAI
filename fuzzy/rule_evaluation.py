# =============================================================================
# RULES EVALUATION: Maps fuzzified inputs to destinations using forward chaining.
# 1. Iterates through the rule set to check for active conditions.
# 2. Calculates rule activation strength by averaging input memberships.
# 3. Aggregates results into a scoring matrix for all valid destinations.
# =============================================================================

from collections import defaultdict

def evaluate_rules(fuzzified_inputs, rules, countries):

    destination_scores = defaultdict(dict)

    for idx, rule in enumerate(rules):
        condition = rule["if"]
        recommended = rule["then"]

        strengths = []

        for variable, label in condition.items():
            if variable in fuzzified_inputs:
                strengths.append(fuzzified_inputs[variable].get(label, 0))

        if not strengths:
            continue

        rule_strength = sum(strengths) / len(strengths)

        for dest in recommended:
            if dest in countries:
                destination_scores[dest][f"r{idx}"] = rule_strength

    return destination_scores
