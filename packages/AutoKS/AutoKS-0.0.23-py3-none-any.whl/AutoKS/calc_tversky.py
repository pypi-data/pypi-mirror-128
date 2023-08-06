#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calc_tversky(
        graph1,
        graph2,
        comparison,
        alpha=0.5,
        detailed=False
):
    """
    calculate Tversky's similarity between graphs.

    there are three types of similarities, see:
    Kopainsky, B., Pirnay-Dummer, P., & Alessi, S. M. (2012). Automated
    assessment of learners' understanding in complex dynamic systems: Automated
    Assessment of Understanding. System Dynamics Review, 28(2), 131-156.
    and
    Pirnay-Dummer P., Ifenthaler D. (2010) Automated Knowledge Visualization and
    Assessment. In: Ifenthaler D., Pirnay-Dummer P., Seel N. (eds)
    Computer-Based Diagnostics and Systematic Analysis of Knowledge. Springer,
    Boston, MA.

    Noted that the "Network overlap" described by Clariana's researches
    equals to the propositional similarity (when alpha=beta=0.5), see:
    Clariana, R. B., Wallace, P. E., & Godshalk, V. M. (2009). Deriving and
    measuring group knowledge structure from essays: The effects of anaphoric
    reference. Educational Technology Research and Development, 57(6), 725-737.

    :param graph1: a NetworkX graph.
    :param graph2: another Networkx graph.
    :param comparison: a string from ['concept', 'propositional', 'semantic']
    specifying which types of similarities to calculate.
    :param alpha: the parameter "alpha" in the Tversky's similarity.
    :param detailed: show detailed information of calculation or not. Default is
    False.
    :return: a number of Tversky's similarity.
    """

    s = None

    assert comparison in ['concept', 'propositional', 'semantic']

    if comparison == 'concept':
        set1, set2 = concept(graph1, graph2)
        s = tversky(set1, set2, alpha)
    elif comparison == 'propositional':
        set1, set2 = propositional(graph1, graph2, alpha, detailed)
        s = tversky(set1, set2, alpha)
    if comparison == 'semantic':
        c_set1, c_set2 = concept(graph1, graph2)
        p_set1, p_set2 = propositional(graph1, graph2, alpha, detailed)
        s = tversky(p_set1, p_set2, alpha) / tversky(c_set1, c_set2, alpha)

    return s


def takefirst(element):
    """
    a function used to sort lists.
    :param element: do not specify this parameter.
    :return: element[0]
    """
    return element[0]


def concept(graph1, graph2):
    """
    part of calculation of the concept similarity.

    :param graph1: a NetworkX graph.
    :param graph2: another NetworkX graph.
    :return: sets of each graph
    """
    return set(graph1.nodes), set(graph2.nodes)


def propositional(graph1, graph2, alpha, detailed=False):
    """
    part of calculation of the propositional similarity.

    :param graph1: a NetworkX graph.
    :param graph2: another NetworkX graph.
    :param alpha: the parameter "alpha" in the Tversky's similarity.
    :param detailed: show detailed information of calculation or not. Default is
    False.
    :return: sets of each graph
    """
    list1 = []
    list2 = []

    allnodes = set(list(graph1.nodes) + list(graph2.nodes))
    allnodes = list(allnodes)

    for edge in list(graph1.edges):
        list1.append((allnodes.index(edge[0]), allnodes.index(edge[1])))
    for edge in list(graph2.edges):
        list2.append((allnodes.index(edge[0]), allnodes.index(edge[1])))

    # sort
    list1.sort(key=takefirst)
    list2.sort(key=takefirst)

    set1 = set(list1)
    set2 = set(list2)

    if detailed:

        print(f"\033[4m\033[36m\nCalculating Tversky's similarity in ratio "
              f"scales\033[0m")
        print(f"\033[36ms = (set1 - set2)/[(set1 - set2) + alpha*(set1 - "
              f"set2) + beta*(set2 - set1)]\n "
              f"alpha={alpha}, beta={1-alpha}\n")

        # set1 & set2
        intersection = content_in_set(set1 & set2, allnodes)
        print('set1 & set2:', intersection)
        print('value of set1 & set2:', len(intersection))

        # set1 - set2
        difference1 = content_in_set(set1 - set2, allnodes)
        print('set1 - set2:', difference1)
        print('value of set1 - set2:', len(difference1))
        difference2 = content_in_set(set2 - set1, allnodes)
        print('set2 - set1:', difference2)
        print('value of set2 - set1:', len(difference2))

        print(f"similarity = {len(intersection)}/"
              f"({len(intersection)} + {alpha}*{len(difference1)} + "
              f"{1-alpha}*{len(difference2)})"
              f"={len(intersection)/(len(intersection)+alpha*len(difference1)+(1-alpha)*len(difference2))}\033[0m")

    return set1, set2


def content_in_set(my_set, allnodes):
    """
    a function used to show detailed information of calculation.

    :param my_set: a set.
    :param allnodes: a list of nodes.
    :return: a set.
    """
    my_set = list(my_set)
    content = []
    for i in range(0, len(my_set)):
        content.append([allnodes[my_set[i][0]], allnodes[my_set[i][1]]])
    return content


def tversky(set1, set2, alpha=0.5):
    """
    calculation of Tversky;s simialrity.

    for Tversky's similarity, see:
    Tversky, A. (1977). Features of similarity. Psychological Review, 84(4),
    327–352.

    :param set1: a set.
    :param set2: another set.
    :param alpha: the parameter "alpha" in Tversky's similarity.
    :return: a number of similarity
    """

    if set1 != set2:
        beta = 1 - alpha
        s = len(set1 & set2) / (len(set1 & set2) +
                                alpha * len(set1 - set2) +
                                beta * len(set2 - set1))
    else:
        s = 1

    s = float('%.4f' % s)

    return s
