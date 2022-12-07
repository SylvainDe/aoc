# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import fractions
import math


def get_quantity_and_chemical(s):
    nb, chem = s.split(" ")
    return (int(nb), chem)


def get_reaction_from_line(l):
    left, mid, right = l.strip().partition(" => ")
    assert mid == " => "
    return (
        [get_quantity_and_chemical(chunk) for chunk in left.split(", ")],
        get_quantity_and_chemical(right),
    )


def get_reactions_from_file(file_path="../../resources/year2019_day14_input.txt"):
    with open(file_path) as f:
        return [get_reaction_from_line(l) for l in f]


def apply_reaction(products, reaction_by_output, integer_recipe):
    for prod, nb in products.items():
        if nb > 0:
            if prod in reaction_by_output:
                chemicals_in, nb_out, = reaction_by_output[prod]
                if integer_recipe:
                    q = math.ceil(nb / nb_out)
                else:
                    q = fractions.Fraction(nb, nb_out)
                products[prod] = nb - nb_out * q
                for n, chem in chemicals_in:
                    products[chem] += q * n
                return True
    return False


def ore_to_make_product(reactions, integer_recipe=True, product=[(1, "FUEL")]):
    reaction_by_output = dict()
    for chemicals_in, (nb_out, chem_out) in reactions:
        assert chem_out not in reaction_by_output
        reaction_by_output[chem_out] = (chemicals_in, nb_out)

    products = collections.Counter({prod: nb for nb, prod in product})
    while apply_reaction(products, reaction_by_output, integer_recipe):
        pass
    for prod, nb in products.items():
        assert prod == "ORE" or nb <= 0
    return products["ORE"]


def max_fuel_prod(reactions, ore=1000000000000):
    ore_per_fuel = ore_to_make_product(reactions, False)
    fuel_estimation = int(ore / ore_per_fuel)
    assert ore_to_make_product(reactions, False, [(fuel_estimation, "FUEL")]) <= ore
    return fuel_estimation


def run_tests():
    reactions = [
        "10 ORE => 10 A",
        "1 ORE => 1 B",
        "7 A, 1 B => 1 C",
        "7 A, 1 C => 1 D",
        "7 A, 1 D => 1 E",
        "7 A, 1 E => 1 FUEL",
    ]
    reactions = [get_reaction_from_line(l) for l in reactions]
    assert ore_to_make_product(reactions) == 31
    reactions = [
        "9 ORE => 2 A",
        "8 ORE => 3 B",
        "7 ORE => 5 C",
        "3 A, 4 B => 1 AB",
        "5 B, 7 C => 1 BC",
        "4 C, 1 A => 1 CA",
        "2 AB, 3 BC, 4 CA => 1 FUEL",
    ]
    reactions = [get_reaction_from_line(l) for l in reactions]
    assert ore_to_make_product(reactions) == 165
    reactions = [
        "157 ORE => 5 NZVS",
        "165 ORE => 6 DCFZ",
        "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
        "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
        "179 ORE => 7 PSHF",
        "177 ORE => 5 HKGWZ",
        "7 DCFZ, 7 PSHF => 2 XJWVT",
        "165 ORE => 2 GPVTF",
        "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",
    ]
    reactions = [get_reaction_from_line(l) for l in reactions]
    assert ore_to_make_product(reactions) == 13312
    assert max_fuel_prod(reactions) == 82892753
    reactions = [
        "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
        "17 NVRVD, 3 JNWZP => 8 VPVL",
        "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
        "22 VJHF, 37 MNCFX => 5 FWMGM",
        "139 ORE => 4 NVRVD",
        "144 ORE => 7 JNWZP",
        "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
        "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
        "145 ORE => 6 MNCFX",
        "1 NVRVD => 8 CXFTF",
        "1 VJHF, 6 MNCFX => 4 RFSQX",
        "176 ORE => 6 VJHF",
    ]
    reactions = [get_reaction_from_line(l) for l in reactions]
    assert ore_to_make_product(reactions) == 180697
    assert max_fuel_prod(reactions) == 5586022
    reactions = [
        "171 ORE => 8 CNZTR",
        "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
        "114 ORE => 4 BHXH",
        "14 VRPVC => 6 BMBT",
        "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
        "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
        "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
        "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
        "5 BMBT => 4 WPTQ",
        "189 ORE => 9 KTJDG",
        "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
        "12 VRPVC, 27 CNZTR => 2 XDBXC",
        "15 KTJDG, 12 BHXH => 5 XCVML",
        "3 BHXH, 2 VRPVC => 7 MZWV",
        "121 ORE => 7 VRPVC",
        "7 XCVML => 6 RJRHP",
        "5 BHXH, 4 VRPVC => 5 LTCX",
    ]
    reactions = [get_reaction_from_line(l) for l in reactions]
    assert ore_to_make_product(reactions) == 2210736
    assert max_fuel_prod(reactions) == 460664


def get_solutions():
    reactions = get_reactions_from_file()
    print(ore_to_make_product(reactions) == 261960)
    print(max_fuel_prod(reactions) == 4366186)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
