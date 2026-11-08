# =============================================================================
# NLP UTILS: Manages context-free grammar (CFG).
# 1. Defines structural rules for parsing travel-related user responses.
# 2. Extracts key linguistic entities (months, budget levels, weather, etc.).
# 3. Maps extracted terms to a normalized numeric scale (1-10) for fuzzy logic.
# =============================================================================


from nltk import CFG, ChartParser

# GRAMMAR
GRAMMAR_TEXT = """
    S -> MONTH_ANSWER | BUDGET_ANSWER | WEATHER_ANSWER | DURATION_ANSWER | DISTANCE_ANSWER | TYPE_ANSWER

    # ================= MONTH ANSWERS =================
    MONTH_ANSWER -> CORE_MONTH
    MONTH_ANSWER -> PRP AUX CORE_MONTH
    MONTH_ANSWER -> PRP AUX PREF CORE_MONTH
    MONTH_ANSWER -> ADV_OPT CORE_MONTH

    CORE_MONTH -> P_IN MONTH_EXPR
    CORE_MONTH -> MONTH_EXPR

    MONTH_EXPR -> MONTH_LIST
    MONTH_EXPR -> SEASON

    MONTH_LIST -> MONTH
    MONTH_LIST -> MONTH SEP MONTH_LIST

    MONTH -> "january" | "february" | "march" | "april" | "may" | "june" | "july" | "august" | "september" | "october" | "november" | "december"

    SEASON -> "spring" | "summer" | "autumn" | "fall" | "winter" | "summertime" | "wintertime"

    # ================= BUDGET ANSWERS =================
    BUDGET_ANSWER -> BUDGET
    BUDGET_ANSWER -> "my" "budget" "is" BUDGET
    BUDGET_ANSWER -> "is" BUDGET | "it's" BUDGET

    BUDGET -> CORE_BUDGET
    BUDGET -> PRP AUX CORE_BUDGET
    BUDGET -> PRP AUX PREF CORE_BUDGET
    BUDGET -> ADV_OPT CORE_BUDGET
    BUDGET -> ADV_OPT PREF CORE_BUDGET

    CORE_BUDGET -> BUDGET_LIST
    CORE_BUDGET -> BUDGET_LIST "budget"
    
    BUDGET_LIST -> BUDGET_LEVEL
    BUDGET_LIST -> "a" BUDGET_LEVEL
    BUDGET_LIST -> MOD BUDGET_LEVEL
    BUDGET_LIST -> RANGE
    BUDGET_LIST -> FLEX
    BUDGET_LIST -> CURRENCY_AMOUNT

    RANGE -> BUDGET_LEVEL SEP BUDGET_LEVEL
    RANGE -> "between" BUDGET_LEVEL SEP BUDGET_LEVEL
    RANGE -> "from" BUDGET_LEVEL "to" BUDGET_LEVEL
    RANGE -> "between" NUM AMOUNT "and" NUM AMOUNT

    MOD -> "about" | "around" | "under" | "over" | "up" "to" | "less than" | "more than" | "a" | "an" | "the"

    FLEX -> "any amount" | "no" "limit" | "not" "important" | "flexible" | "doesn't matter"

    MODIFIER -> "very" | "quite" | "rather" | "super" | "extremely" | "fairly"

    BUDGET_LEVEL -> "cheap" | "low" | "affordable" | "moderate" | "medium" | "reasonable" | "generous" | "high" | "expensive" | "luxury" | "budget" | "economical" | "average" | "mid"

    CURRENCY_AMOUNT -> NUM AMOUNT
    AMOUNT -> "dollars" | "euros" | "pounds" | "$" | "€" | "£"

    # ================= WEATHER ANSWERS =================
    WEATHER_ANSWER -> CORE_WEATHER
    WEATHER_ANSWER -> PRP AUX CORE_WEATHER
    WEATHER_ANSWER -> PRP AUX PREF CORE_WEATHER
    WEATHER_ANSWER -> ADV_OPT CORE_WEATHER
    WEATHER_ANSWER -> ADV_OPT PREF CORE_WEATHER

    CORE_WEATHER -> WEATHER_LIST
    CORE_WEATHER -> WEATHER_LIST "weather"

    WEATHER_LIST -> WEATHER1
    WEATHER_LIST -> "a" WEATHER1

    WEATHER1 -> WEATHER
    WEATHER1 -> WEATHER SEP WEATHER_LIST

    WEATHER -> "cold" | "cool" | "warm" | "hot" | "mild" | "sunny" | "rainy" | "dry" | "windy" | "humid" | "cloudy" | "clear" | "breezy" | "chilly" | "temperate" | "tropical"

    # ================= DURATION ANSWERS =================
    DURATION_ANSWER -> "just" DURATION
    DURATION_ANSWER -> DURATION
    
    DURATION -> CORE_DURATION
    DURATION -> PRP AUX CORE_DURATION
    DURATION -> PRP AUX PREF CORE_DURATION
    DURATION -> ADV_OPT CORE_DURATION
    DURATION -> ADV_OPT PREF CORE_DURATION
    
    CORE_DURATION -> DURATION_LIST
    CORE_DURATION -> DURATION_LIST "duration"
    CORE_DURATION -> DURATION_LIST "trip"
    CORE_DURATION -> DURATION_LIS "experience"

    DURATION_LIST -> DURATION_LEVEL
    DURATION_LIST -> DURATION_RANGE
    DURATION_LIST -> DURATION_DAYS

    DURATION_LEVEL -> "short" | "brief" | "quick" | "medium" | "moderate" | "long" | "extended" | "lengthy" | "very" "long"

    DURATION_RANGE -> "a" "few" "days" | "a" "week" | "two" "weeks" | "a" "month" | "two" "months" 

    DURATION_DAYS -> NUM "days" | NUM "weeks"

    # ================= DISTANCE ANSWERS =================
    DISTANCE_ANSWER -> CORE_DISTANCE
    DISTANCE_ANSWER -> PRP AUX CORE_DISTANCE
    DISTANCE_ANSWER -> PRP AUX PREF CORE_DISTANCE
    DISTANCE_ANSWER -> ADV_OPT CORE_DISTANCE
    DISTANCE_ANSWER -> ADV_OPT PREF CORE_DISTANCE

    CORE_DISTANCE -> DISTANCE_LIST
    CORE_DISTANCE -> DISTANCE_LIST "distance"
    CORE_DISTANCE -> DISTANCE_LIST "destination" | DISTANCE_LIST "destinations"
    CORE_DISTANCE -> DISTANCE_LIST "travel"

    DISTANCE_LIST -> DISTANCE
    DISTANCE_LIST -> "a" DISTANCE

    DISTANCE -> DISTANCE_LEVEL
    DISTANCE -> DISTANCE_RANGE 

    DISTANCE_LEVEL -> "near" | "close" | "local" | "here" | "regional" | "mid" | "middle" | "medium" | "far" | "far" "away" | "long" "distance" | "distant" | "remote" | "very" "far"

    DISTANCE_RANGE -> "short" "flight" | "medium" "flight" | "long" "flight" | "driving" "distance"

    # ================= TYPE/VACATION STYLE ANSWERS =================
    TYPE_ANSWER -> CORE_TYPE
    TYPE_ANSWER -> PRP AUX CORE_TYPE
    TYPE_ANSWER -> PRP AUX PREF CORE_TYPE
    TYPE_ANSWER -> ADV_OPT CORE_TYPE
    TYPE_ANSWER -> ADV_OPT PREF CORE_TYPE

    CORE_TYPE -> TYPE_LIST
    CORE_TYPE -> TYPE_LIST "vacation"
    CORE_TYPE -> TYPE_LIST "trip"

    TYPE_LIST -> VACATION_TYPE1
    TYPE_LIST -> "a" VACATION_TYPE
    
    VACATION_TYPE1 -> VACATION_TYPE
    VACATION_TYPE1 -> VACATION_TYPE SEP TYPE_LIST

    VACATION_TYPE -> "relaxing" | "adventure" | "cultural" | "beach" | "mountain" | "city" | "countryside" | "romantic" | "family" | "solo" | "luxury" | "backpacking" | "road trip" | "cruise" | "ski" | "spa" | "food" | "historical" | "eco" | "volunteer" | "nature" | "hiking" | "activities"

    # ================= SHARED / COMPACT =================
    PRP -> "i" | "we" | "us" | "my" | "our"
    
    AUX -> "can" | "would" | "usually" | "want" | "like" | "prefer" | "need" | "enjoy" | "love"
    
    PREF -> "a"
    PREF -> GO
    PREF -> AUX2
    PREF -> AUX2 GO
    PREF -> AUX2 "to" GO

    AUX2 -> "prefer" | "like" | "want" | "would" | "need"
    GO -> VERB P_IN
    GO -> "to" VERB P_IN
    VERB -> "going" | "go" | "traveling" | "travel" | "doing" | "do" | "visiting" | "visit" | "taking" | "take"

    ADV_OPT -> "preferably" | "ideally" | "if possible" | "honestly" | "well" | "probably" | "maybe"

    P_IN -> "in" | "during" | "between" | "for"
    SEP -> "and" | "or" | "," | "but"
    NUM -> "1" | "2" | "3" | "4" | "5" | "6" | "7" | "100" | "200" | "500" | "1000" | "1500" | "2000" | "3000" | "5000" | "10000" | "one" | "two" | "three" | "four" | "five" | "six" | "seven"
"""

# PARSER INITIALIZATION
def create_parser():
    grammar = CFG.fromstring(GRAMMAR_TEXT)
    return ChartParser(grammar)

# SAFE PARSE FUNCTION
def safe_parse(text, parser):
    """
    Parses text with the provided parser, capturing errors.
    
    Args:
        text: Text to parse
        parser: Initialized NLTK parser
        
    Returns:
        List of parse trees (empty if there's an error)
    """
    tokens = text.lower().split()
    try:
        return list(parser.parse(tokens))
    except ValueError:
        return []
    except Exception as e:
        print(f"Unexpected parsing error: {e}")
        return []

def pretty_join(words):
    """
    Joins a list of words into a natural English phrase.
    
    Args:
        words: List of words
        
    Returns:
        Formatted string: "word", "word1 and word2", or "word1, word2 and word3"
    """
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    if len(words) == 2:
        return f"{words[0]} and {words[1]}"
    return ", ".join(words[:-1]) + f" and {words[-1]}"


# EXTRACTION FUNCTIONS
def extract_months(tree):
    months = []
    for subtree in tree.subtrees():
        if subtree.label() in {"MONTH", "SEASON"}:
            months.extend(subtree.leaves())
    return months

def extract_budget(tree):
    budget = []
    for subtree in tree.subtrees():
        if subtree.label() in {"BUDGET_LEVEL", "MOD", "FLEX", "CURRENCY_AMOUNT", "NUM", "AMOUNT"}:
            budget.extend(subtree.leaves())
    return budget

def extract_weather(tree):
    weather = []
    for subtree in tree.subtrees():
        if subtree.label() == "WEATHER":
            weather.extend(subtree.leaves())
    return weather

def extract_duration(tree):
    duration = []
    for subtree in tree.subtrees():
        if subtree.label() in {"DURATION_LEVEL", "DURATION_RANGE", "DURATION_DAYS"}:
            duration.extend(subtree.leaves())
    return duration

def extract_distance(tree):
    distance = []
    for subtree in tree.subtrees():
        if subtree.label() in {"DISTANCE_LEVEL", "DISTANCE_RANGE"}:
            distance.extend(subtree.leaves())
    return distance

def extract_type(tree):
    vacation_type = []
    for subtree in tree.subtrees():
        if subtree.label() == "VACATION_TYPE":
            vacation_type.extend(subtree.leaves())
    return vacation_type


# NUMBER CONVERSION FUNCTIONS
def month_to_number(months):
    """Convert months/seasons to numeric values (1 to 12)"""

    if not months:
        return 6.5

    if isinstance(months, str):
        months = months.split()

    month_map = {
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
        "winter": 1, "wintertime": 1,
        "spring": 4,
        "summer": 7, "summertime": 7,
        "autumn": 10, "fall": 10
    }
    values = []

    for m in months:
        if m in month_map:
            values.append(month_map[m])

    if values:
        return sum(values) / len(values)
    else:
        return 6.5

def budget_to_number(budget):
    if not budget:
        return 3

    if isinstance(budget, str):
        budget = budget.split()

    budget_map = {
        "cheap": 1, 
        "low": 2, "economical": 2,
        "affordable": 4, "reasonable": 4.5,
        "average": 5, "moderate": 5.5, "medium": 5.5, "mid": 5.5,
        "generous": 6.5,
        "high": 8.5,
        "expensive": 9, "luxury": 10,

        "flexible": 5, "doesn't matter": 5.5, "no limit": 7.5, "any amount": 7.5
    }

    for word in budget:
        if word.isdigit():
            amount = int(word)
            if amount <= 500: return 1
            if amount <= 1000: return 1.5
            if amount <= 2000: return 2
            if amount <= 3000: return 3
            return 4

        if word in budget_map:
            return budget_map[word]

    return 3

def weather_to_number(weather):
    if not weather:
        return 7

    if isinstance(weather, str):
        weather = weather.split()

    weather_map = {
        "cold": 1, 
        "chilly": 2,
        "cool": 3, "rainy": 3.5,
        "windy": 4, "cloudy": 4, "breezy": 4.5,
        "mild": 5.5, "temperate": 5.5,
        "clear": 6,
        "warm": 7, "dry": 7, "sunny": 7.5,
        "humid": 8.5, "hot": 9,
        "tropical": 10
    }

    values = []

    for word in weather:
        if word in weather_map:
            values.append(weather_map[word])

    if values:
        return sum(values) / len(values)
    else:
        return 7

def duration_to_number(duration):
    if not duration:
        return 6
    
    if isinstance(duration, str):
        duration = duration.split()


    phrase_map = {
        "short": 2, "quick": 2.5, 
        "brief": 3, "a few days": 3.5,
        "a week": 5, "medium": 5.5, "moderate": 6,
        "two weeks": 7, "long": 8.5,
        "very long": 9, "several weeks": 9, "extended": 9, "lengthy": 9.5, "a month": 10
    }

    for word, number in phrase_map.items():
        if word in duration:
            return number

    for word in duration:

        if word.isdigit():

            num = int(word)

            if "week" in duration:
                return min(10, num * 7)
           
            if "day" in duration:
                return max(2, min(10, num))

    return 6

def distance_to_number(distance):
    if not distance:
        return 4

    if isinstance(distance, str):
        distance = distance.split()

    distance_map = {
        "here": 1, "local": 2, 
        "close": 3, "near": 3.5, "regional": 3.5,
        "driving distance": 4, "short flight": 4.5,
        "mid": 5, "middle": 5.5, "medium": 5.5,
        "far": 6, "medium flight": 6.5,
        "remote": 7, "long distance": 7.5, 
        "far away": 8, "distant": 8,
        "very far": 9, "long flight": 10
    }

    for word in distance:
        if word in distance_map:
            return distance_map[word]

    return 4

def type_to_number(types):
    if not types:
        return 3

    if isinstance(types, str):
        types = types.split()

    type_map = {
        
        "spa": 1, 
        "beach": 2, "cruise": 2, "luxury": 2.5,
        "romantic": 3, "relaxing": 3.5,
        "historical": 4, "cultural": 4.5, "food": 4.5,
        "city": 5, "family": 5.5, "volunteer": 5.5,
        "solo": 6, "eco": 6, "countryside": 6.5,
        "nature": 7, "mountain": 7,
        "hiking": 8, "activities": 8, "road trip": 8.5,
        "adventure": 9, "backpacking": 9, "ski": 9,
        "wildlife": 10
    }


    values = []
    
    for type in types:
        if type in type_map:
            values.append(type_map[type])
    
    if values:
        return sum(values) / len(values)
    else:
        return 3


# QUESTIONS
questions = [
        {
            'key': 'time',
            'question': "When would you like to go on vacation?",
            'example': "Example: 'I enjoy going during summer'",
            'extract_func': extract_months
        },
        {
            'key': 'budget',
            'question': "What's your budget for this vacation?",
            'example': "Example: 'I would like between cheap and medium'",
            'extract_func': extract_budget
        },
        {
            'key': 'weather',
            'question': "What kind of weather do you prefer?",
            'example': "Example: 'I prefer warm and sunny weather'",
            'extract_func': extract_weather
        },
        {
            'key': 'duration',
            'question': "How long would you like your vacation to be?",
            'example': "Example: 'We want a short trip'",
            'extract_func': extract_duration
        },
        {
            'key': 'distance',
            'question': "How far are you willing to travel?",
            'example': "Example: 'I prefer a close destinations'",
            'extract_func': extract_distance
        },
        {
            'key': 'vacation_type',
            'question': "What type of vacation are you looking for?",
            'example': "Example: 'Preferably a relaxing and cultural vacation'",
            'extract_func': extract_type
        }
    ]

def number_questions():
    return len(questions)

# RESULTS
def results(responses):

    numbers = {}

    for key, value in responses.items():
        if key == 'time':
            numbers[key] = month_to_number(value)

        elif key == 'budget':
            numbers[key] = budget_to_number(value)
        
        elif key == 'weather':
            numbers[key] = weather_to_number(value)
        
        elif key == 'duration':
            numbers[key] = duration_to_number(value)
        
        elif key == 'distance':
            numbers[key] = distance_to_number(value)
        
        elif key == 'vacation_type':
            numbers[key] = type_to_number(value)

    return numbers
