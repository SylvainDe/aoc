# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_ingredients_from_line(line):
    beg, sep, end = line.partition(" (contains ")
    return tuple(beg.split(" ")), end[:-1].split(", ")


def get_ingredients_from_file(file_path="day21_input.txt"):
    with open(file_path) as f:
        return [get_ingredients_from_line(l.strip()) for l in f]


def identify_allergens(ingredients):
    allergen_sources = dict()
    for ingred, allergens in ingredients:
        for aller in allergens:
            allergen_sources.setdefault(aller, []).append(ingred)
    allergen_cand = {
        aller: set.intersection(*[set(l) for l in meta_list])
        for aller, meta_list in allergen_sources.items()
    }
    ident_ingred = dict()
    change = True
    while change:
        change = False
        for aller, cand in list(allergen_cand.items()):
            candidates = cand - set(ident_ingred)
            assert candidates
            if len(candidates) == 1:
                ident_ingred[candidates.pop()] = aller
                allergen_cand.pop(aller)
                change = True
    if allergen_cand:
        print("Not all allergens have been identified")
    return ident_ingred


def get_nb_safe_ingredients(ingredients):
    ident_ingred = identify_allergens(ingredients)
    return sum(i not in ident_ingred for ingred, _ in ingredients for i in ingred)


def get_canonical_dangerous_list(ingredients):
    ident_ingred = identify_allergens(ingredients)
    return ",".join(sorted(ident_ingred, key=ident_ingred.get))


def run_tests():
    example1 = [
        "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
        "trh fvjkl sbzzf mxmxvkd (contains dairy)",
        "sqjhc fvjkl (contains soy)",
        "sqjhc mxmxvkd sbzzf (contains fish)",
    ]
    ingredients = [get_ingredients_from_line(l) for l in example1]
    assert get_nb_safe_ingredients(ingredients) == 5
    assert get_canonical_dangerous_list(ingredients) == "mxmxvkd,sqjhc,fvjkl"


def get_solutions():
    ingredients = get_ingredients_from_file()
    print(get_nb_safe_ingredients(ingredients) == 2317)
    print(
        get_canonical_dangerous_list(ingredients)
        == "kbdgs,sqvv,slkfgq,vgnj,brdd,tpd,csfmb,lrnz"
    )


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
