# =============================================================================
# INFERENCE ENGINE: Main entry point for the fuzzy logic system.
# 1. Loads configuration data for countries, fuzzy sets, and logic rules.
# 2. Coordinates the fuzzification, rule evaluation, and defuzzification pipeline.
# 3. Determines the best destination based on the highest calculated score.
# =============================================================================

import json
from fuzzy.fuzzification import fuzzify_user_input
from fuzzy.rule_evaluation import evaluate_rules
from fuzzy.defuzzification import defuzzify


def recommend_destination(user_input):
    with open("fuzzy/countries.json") as f:
        countries = json.load(f)

    with open("fuzzy/rules.json") as f:
        rules = json.load(f)

    with open("fuzzy/fuzzy_sets.json") as f:
        fuzzy_sets = json.load(f)

    fuzzified_inputs = fuzzify_user_input(user_input, fuzzy_sets) #fuzzification

    scores = evaluate_rules(fuzzified_inputs, rules, countries) # rule evaluation

    def_scores = defuzzify(scores) # defuzzification

    if not def_scores:
        return None, {}

    best = max(def_scores, key=def_scores.get) #choose best destination

    return best, def_scores