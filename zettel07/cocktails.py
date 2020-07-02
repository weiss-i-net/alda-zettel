import json
import re
import time

def read_json_to_dict(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def write_dict_to_json(dict_to_write, filename):
    with open(filename, 'w') as file:
        json.dump(dict_to_write, file, indent=4, sort_keys=True)

def normalize_string(ingredient):
    ingre_copy = str(ingredient)
    stripped = re.sub(' *\(.*?($|\)) *'
                      '|[^a-z0-9 äüöß]'
                      '| *\\b\w*(kalt|braun|kühl|süße|weiße|dunkle|trocken|geschlagen|gerieben|geschält|entkernt|gewürfelt)\w*\\b *'
                      '| *\\b(oder|aus|zum|mit)\\b.*'
                      '| *(blue|mekong|bourbon|single malt|gold|silver|direkt|schlag|steif|meer|ersatz|blüten|coconut rum) *', '', ingredient.lower())

    DIRECT_REPLACEMENTS = { 'orange juice': 'orangensaft',
                            'eiswürfel zerstoßene': 'crushed ice',
                            'sodawasser': 'mineralwasser',
                            'triple sec': 'curacao',
                            'rosenblätter': 'rosenblüte',
                            'maraschinokirsche': 'cocktailkirsche',
                            'schokoladenraspel': 'schokostreusel' }
    if stripped in DIRECT_REPLACEMENTS:
        stripped = DIRECT_REPLACEMENTS[stripped]

    if stripped == '':
        raise ValueError(f'normalize_string: Resulting string is empty. Input: {ingre_copy}')
    return stripped

def all_ingredients(recipes):
    ingre = set()
    for recipe in recipes.values():
        for ingredient in recipe['ingredients']:
            ingre.add(normalize_string(ingredient))
    return ingre

def cocktails_inverse(recipes):
    inverse_ingre = { ingre: [] for ingre in all_ingredients(recipes) }
    for name, recipe in recipes.items():
        for ingredient in recipe['ingredients']:
            inverse_ingre[normalize_string(ingredient)].append(name)
    return inverse_ingre

def get_ingre_freq(inverse_recipes):
    ingre_freq_list = [(ingre, len(names)) for ingre, names in inverse_recipes.items()]
    ingre_freq_list.sort(key=lambda x: x[1], reverse=True)
    return ingre_freq_list

IGNORE_SET = { 'cocktailkirsche', 'cocktailtomate',   'eisbonbos',  'gurkenscheiben',
               'kokosraspel',     'limettenscheiben', 'rosenblüte', 'schokostreusel',
               'süßigkeiten' }

COMMON_SET = { 'alkohol', 'bier',      'crushed ice',   'ei',
               'eigelb',  'eiswürfel', 'eiweiß',        'honig',
               'kaffee',  'milch',     'mineralwasser', 'nutella',
               'obst',    'pfeffer',   'salz',          'schnaps',
               'wasser',  'zucker' }

def possible_cocktails(inverse_recipes, available_ingredients):
    available_ingredients = { normalize_string(ingre) for ingre in available_ingredients } | IGNORE_SET | COMMON_SET

    possible_cocktails = set()
    impossible_cocktails = set()

    for ingredient, cocktail_list in inverse_recipes.items():
        possible_cocktails.update(cocktail_list)
        if ingredient not in available_ingredients:
            impossible_cocktails.update(cocktail_list)

    return possible_cocktails - impossible_cocktails

class FixedLengthSubset:
    """ Helper Class to get all fixed length subsets of an array.

    Using a bit mask that is updated with bitwise operations."""
    def __init__(self, data, subset_length=4):
        self._start_bits = (1 << subset_length) - 1
        self._bits = self._start_bits
        self._data = data
        self._max_bits = 1 << len(data)

    def _increment_bits_lexographically(self):
        """ from https://graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation """
        t = (self._bits | (self._bits - 1)) + 1
        self._bits = t | ((((t & -t) // (self._bits & -self._bits)) >> 1) - 1)

    def _get_curr_subset(self):
        bit_mask = self._bits
        def next_bit(_):
            nonlocal bit_mask
            bit = bit_mask & 1
            bit_mask >>= 1
            return bit
        return list(filter(next_bit, self._data))

    def __iter__(self):
        self._bits = self._start_bits
        return self

    def __next__(self):
        if self._bits >= self._max_bits:
            raise StopIteration
        subset = self._get_curr_subset()
        self._increment_bits_lexographically()
        return subset

def optimal_ingredients(inverse_recipes, ingredient_count=5, searchtime=10):
    """ Determines the optimal combination of an amount of ingredients.

    Checks the most common ingredients first and then adds increasingly uncommon ingredients.
    Stops after searchtime is reached or all combinations have been checked.

    Cocktails with ingredients that appear in less then 20 cocktails are removed before the
    search. This yields a 151% performance increase.
    Testing has shown that these ingredients typically dont appear in the solution.
    (for 5 ingrediants, champagner was the most uncommon, appearing in 31 cocktails)
    """

    # filtering out common and unimportant ingrediants
    freq_list = list(filter(lambda elem: elem[0] not in IGNORE_SET | COMMON_SET, get_ingre_freq(inverse_recipes)))

    # filtering out cocktails with uncommon ingrediants
    bad_cocktails = set()
    for pair in freq_list:
        if pair[1] <= 20:
            bad_cocktails.update(inverse_recipes[pair[0]])
    for ingre, cocktails in list(inverse_recipes.items()):
        inverse_recipes[ingre] = set(cocktails)
        inverse_recipes[ingre] -= bad_cocktails
        if len(inverse_recipes[ingre]) == 0:
            del inverse_recipes[ingre]

    # main search
    start_time = time.time()
    checked_combinations = 1

    sorted_ingre = [i[0] for i in freq_list]
    best_guess = sorted_ingre[:ingredient_count], len(possible_cocktails(inverse_recipes, sorted_ingre[:ingredient_count]))

    for ingre_rank in range(ingredient_count, len(sorted_ingre)):
        # testing subsets of an increasingly big range
        subsets = FixedLengthSubset(sorted_ingre[:ingre_rank], ingredient_count - 1)
        for curr_subset in subsets:
            # the new elem is appeneded to all subsets of old elems with length n-1,
            # this way only new combinations are tested
            curr_subset.append(sorted_ingre[ingre_rank])

            curr_guess = curr_subset, len(possible_cocktails(inverse_recipes, curr_subset))
            if curr_guess[1] > best_guess[1]:
                best_guess = curr_guess

            checked_combinations += 1
            if time.time() - start_time > searchtime:
                print(f'Checked {checked_combinations} combinations in {searchtime} seconds.')
                return best_guess
    return best_guess


def main():
    recipes = read_json_to_dict('cocktails.json')

    print(f'Total amount of ingredients: {len(all_ingredients(recipes))}\n')

    inverse_recipes = cocktails_inverse(recipes)

    write_dict_to_json(inverse_recipes, 'cocktails_inverse.json')

    print('Most used ingredients:')
    for pair in get_ingre_freq(inverse_recipes)[:15]:
        print(pair)

    available_ingredients = ['Gin', 'Schlagsahne', 'Blue Curacao', 'Wodka', 'Grapefruitsaft']
    print(f'\nPossible Cocktails with the ingredients {available_ingredients}:\n'
          f'{possible_cocktails(inverse_recipes, available_ingredients)}\n')

    print('Calculating optimal combination of 5 ingredients... (20 seconds)')
    best_ingredients, cocktail_count = optimal_ingredients(inverse_recipes, 5, 20)
    print(f'{best_ingredients} can be used for {cocktail_count} diffrent cocktails.')

    # Result for 10 min without filtering cocktails:
    # Checked 1675714 combinations in 600 seconds.
    # ['orangensaft', 'wodka', 'curacao', 'baileys irish cream', 'champagner'] can be used for 13 diffrent cocktails.


if __name__ == '__main__':
    main()
