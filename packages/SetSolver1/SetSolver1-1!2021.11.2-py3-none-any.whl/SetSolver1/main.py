from itertools import chain, combinations, combinations_with_replacement


def union(x, y):
    """
    German: Vereinigungsmenge
    :type x: set[frozenset | int]
    :type y: set[frozenset | int]
    :rtype: set[frozenset | int]
    """
    x_copy = x.copy()
    x_copy.update(y)
    return x_copy


def complement(x, y):
    """
    German: Komplement - Subtraktion von Mengen
    :type x: set[frozenset | int]
    :type y: set[frozenset | int]
    :rtype: set[frozenset | int]
    """
    return x.difference(y)


def intersection(x, y):
    """
    German: Schnittmenge
    :type x: set[frozenset | int]
    :type y: set[frozenset | int]
    :rtype: set[frozenset | int]
    """
    return x.intersection(y)


def power_set(x):
    """
    German: Potenzmenge
    :type x: set[frozenset | int]
    :rtype: set[frozenset | int]
    """
    if size(x) >= (overflow/2):
        return set()
    return set([frozenset(y) for y in chain.from_iterable(combinations(x, i) for i in range(len(x) + 1))])


def composition(x, y):
    """
    TODO optimization
    German: Verkettung
    :type x: set[frozenset | int | tuple]
    :type y: set[frozenset | int | tuple]
    :rtype: set[frozenset | int | tuple]
    """
    liste = list()
    for x1 in x:
        for y1 in y:
            if x1[1] == y1[0]:
                liste.append((x1[0], y1[1]))
    return set(liste)


def converse_relation(x):
    """
    TODO optimization
    German: Inverse (Umkehrrelation)
    :type x: set[frozenset | int | tuple]
    :rtype: set[frozenset | int | tuple]
    """
    return set([(x1[1], x1[0]) for x1 in x])


def reflexive_closure(x):
    """
    TODO optimization
    German: Reflexive Hülle
    :type x: set[frozenset | int | tuple]
    :rtype: set[frozenset | int | tuple]
    """
    return set(list(x) + [(x3, x3) for x3 in set([x1[x2] for x2 in range(2) for x1 in x])])


def transitive_closure(x):
    """
    TODO optimization
    German: Transitive Hülle
    :type x: set[frozenset | int | tuple]
    :rtype: set[frozenset | int | tuple]
    """
    # {(1 , 1) , (2 , #3#) , (#3# , 1)} -> {(1 , 1) , #(2 , 1)# , (2 , 3), (3 , 1)}
    return set(list(x) + [(x1[0], x2[1]) for x2 in x for x1 in x if x1[1] == x2[0]])


def tools(t, x, y):
    """
    :type t: int
    :type x: set[frozenset | int]
    :type y: set[frozenset | int]
    :rtype: set[frozenset | int]
    """
    match t:
        case 0:
            return union(x, y)
        case 1:
            return complement(x, y)
        case 2:
            return complement(y, x)
        case 3:
            return intersection(x, y)
        case 4:
            return composition(x, y)
        case 5:
            return composition(y, x)
        case 6:
            return power_set(x)
        case 7:
            return power_set(y)
        case 8:
            return converse_relation(x)
        case 9:
            return converse_relation(y)
        case 10:
            return reflexive_closure(x)
        case 11:
            return reflexive_closure(y)
        case 12:
            return transitive_closure(x)
        case 13:
            return transitive_closure(y)
        case _:
            raise ValueError("value not found")


def s_tools(t, x, y):
    """
    :type t: int
    :type x: str
    :type y: str
    :rtype: str
    """

    match t:
        case 0:
            return "("+x+"+"+y+")"
        case 1:
            return "("+x+"-"+y+")"
        case 2:
            return "("+y+"-"+x+")"
        case 3:
            return "("+x+"&"+y+")"
        case 4:
            return "("+x+"."+y+")"
        case 5:
            return "("+y+"."+x+")"
        case 6:
            return "pow("+x+")"
        case 7:
            return "pow("+y+")"
        case 8:
            return "inverse("+x+")"
        case 9:
            return "inverse("+y+")"
        case 10:
            return "reflexive_cl("+x+")"
        case 11:
            return "reflexive_cl("+y+")"
        case 12:
            return "transitive_cl("+x+")"
        case 13:
            return "transitive_cl("+y+")"
        case _:
            raise ValueError("value not found")


def size(x):
    """
    :type x: set[frozenset | int] | frozenset
    :rtype: int
    """
    y = 0
    for item in x:
        if type(item) == set or type(item) == frozenset:
            y += size(item)
        y += 1
    return y


def format_set(x):
    """
    :type x: set[frozenset | int]
    :rtype: str
    """

    return str(x).replace("frozenset()", "{}").replace("set()", "{}").replace("frozenset(", "").replace(")", "")


def format_way(x, const_sets, results):
    """
    :type x: list[int, set | None, set | None] | None]
    :type const_sets: dict[str, set[frozenset | int]]
    :type results: list[tuple[set, list[int, set | None, set | None] | None]]
    :rtype: str
    """
    # [c, x, y]
    way = list()
    if x[1] is None:
        way.append("")
    elif x[1] in const_sets.values():
        way.append(list(const_sets.keys())[list(const_sets.values()).index(x[1])])
    else:
        for y in results:
            if x[1] == y[0]:
                way.append(format_way(y[1], const_sets, results))
                break
        if len(way) == 0:
            way.append("")
            print(x)
            input("error 1")

    if x[2] is None:
        way.append("")
    elif x[2] in const_sets.values():
        way.append(list(const_sets.keys())[list(const_sets.values()).index(x[2])])
    else:
        for y in results:
            if x[2] == y[0]:
                way.append(format_way(y[1], const_sets, results))
                break
        if len(way) == 1:
            way.append("")
            print(x)
            input("error 2")
    debug_print("way: " + str(way))
    return s_tools(x[0], way[0], way[1])


def check_set(check, way, const_sets, results):
    """
    :type check: set[frozenset | int]
    :type way: list[int, set, set]
    :type const_sets: dict[str, set[frozenset | int]]
    :type results: list[tuple[set, list[int, set | None, set | None] | None]]
    """
    if size(check) <= overflow and check not in [x[0] for x in results]:
        debug_print(format_way(way, const_sets, results) + " --> " + format_set(check))
        results.append((check, way))


def unique_set(x):
    """
    :type x: dict[str, set[frozenset | int]]
    :rtype: dict[str, set[frozenset | int]]
    """
    temp = list()
    for y in x.values():
        if y not in temp:
            temp.append(y)
        else:
            raise ValueError('the dictionary values of set constants must be unique')
    return x


def get_valid_results(const_sets, result, results):
    """
    :type const_sets: dict[str, set[frozenset | int]]
    :type result: set[frozenset | int]
    :type results: list[tuple[set, list[int, set | None, set | None] | None]]
    :return: list[set]
    """
    valid_results = list()
    for a, b in results:
        if result == a:
            valid_results.append(a)
            print("Calculated result:" + format_way(b, const_sets, results) + " --> " + format_set(a))
    return valid_results


def debug_print(x):
    """
    :type x: str
    """
    print(x) if DEBUG else None


def search(const_sets, result, not_allowed=None):
    """
    :type const_sets: dict[str, set[frozenset | int | tuple]]
    :type result: set[frozenset | int | tuple]
    :type not_allowed: list
    :rtype: list[set] | None
    """
    if not_allowed is None:
        not_allowed = [4, 5, 8, 9, 10, 11, 12, 13]
    const_sets = unique_set(const_sets)
    results: list[tuple[set, list[int, set | None, set | None] | None]] = [(x, None) for x in const_sets.values()]
    for len_obj in range(range_int):
        print(str(round((len_obj/(range_int-1))*100)) + "% / " + str(len(results)))
        for x, _ in results.copy():
            for y in [x for x in range(14) if x not in not_allowed]:
                for z in const_sets.values():
                    new = tools(y, x, z)
                    check_set(new, [y, x, z], const_sets, results)
        valid_results = get_valid_results(const_sets, result, results)
        if len(valid_results) > 0:
            return valid_results

    for len_obj in range(range_int):
        print("all: " + str(round((len_obj/(range_int-1))*100)) + "% / " + str(len(results)))
        temp_results_list_for_power_set = results.copy()
        for (x, _), (y, _) in combinations_with_replacement(results, 2):
            for c in [x for x in range(14) if x not in not_allowed + [6, 7]]:
                new = tools(c, x, y)
                check_set(new, [c, x, y], const_sets, results)
        if 6 not in not_allowed:
            for x, _ in temp_results_list_for_power_set:
                new = power_set(x)
                check_set(new, [6, x, None], const_sets, results)
        valid_results = get_valid_results(const_sets, result, results)
        if len(valid_results) > 0:
            return valid_results
    print("Nothing found :(")
    return None


overflow = 30
range_int = 20
DEBUG = False
