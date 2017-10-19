"""
Script to check traders names by finding matches in a dictionary, 
adding new matches and new names as they are encountered.

Clement Suavet
clement.suavet@sei-international.org
2017
"""

import os
import sys

from difflib import get_close_matches

fin_name = sys.argv[1]
fout_name = sys.argv[2]


def load_trader_names():
    """
    Returns dictionary of trader names:
    {wrong_name: correct_name}
    """
    names_dict = {}
    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/traders.csv', 'r') as fin:
        for line in fin:
            item = line.rstrip().split(';')
            name, main_name = item[:2]
            names_dict[name] = main_name
    return names_dict


def check_trader_name(name_to_check, names_dict):
    """
    Returns correct name if name_to_check in dictionary;
    looks for match by fuzzy string matching if no exact match;
    lets user pick name from a list, or add new name to dictionary.
    """

    name_to_check = name_to_check.upper()

    # name already in dictionary
    if name_to_check in names_dict:
        return names_dict[name_to_check]
    
    names_list = sorted(set(names_dict.keys()))

    if 'ORDER OF ' in name_to_check:
        name_to_check_mod = name_to_check[name_to_check.index('ORDER OF ')+9:]
    else:
        name_to_check_mod = name_to_check

    # check for approximate match
    print
    print 80 * "_"
    print "Looking for match for name:", name_to_check
    M = get_close_matches(name_to_check_mod, names_list, 24)

    # no close match found
    if len(M) == 0:
        choice = ''

    # at least one close match found
    else:
        # print name matches
        for i, n in enumerate(M):
            print str(i+1) + ': ' + M[i]
        # let user choose correct name
        choice = raw_input(
            "Select number or press RETURN if no match...\n")
        try:
            chosen_name = names_dict[M[int(choice) - 1]]
            names_dict[name_to_check] = chosen_name
        except:
            choice = ''

    # no match found by string matching, select from list of all nodes
    if choice == '':
        print "Select name from list"
        try:
            a = 0
            end = False
            first_letter = name_to_check_mod[0]
            count = 0
            for n in names_list:
                try:
                    if n[0] == first_letter:
                        names_list = names_list[count:] + names_list[:count]
                        break
                except:
                    pass
                count += 1
            L = zip(names_list, range(len(names_list)))
            while choice == '':
                print name_to_check, '\n'
                if a > len(M):
                    end = True
                for n, c in L[a:(a+24)]:
                    print c, ' : ', n
                choice = raw_input(
                    "Enter number to select name, press return to show "
                    "more, 'q' to abort, "
                    "or any other key to add new name to dictionary...\n").upper()
                a += 24
            if choice == 'Q':
                return None
            # valid selection
            try:
                chosen_name = names_dict[L[int(choice)][0]]
                names_dict[name_to_check] = chosen_name
            # invalid input
            except:
                raise ValueError
        # no match: create new record
        except ValueError:
            chosen_name = name_to_check
            names_dict[name_to_check] = chosen_name
    
    # update file
    with open(os.path.dirname(os.path.abspath(__file__)) + '/traders.csv', 'w') as fout:
        for name in sorted(names_dict.keys()):
            fout.write(name + ';' + names_dict[name] + '\n')
    
    return chosen_name



if __name__ == "__main__":
    names_dict = load_trader_names()
    
    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/' + fin_name, 'r') as fin:
        names_to_check = [line.rstrip() for line in fin]

    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/' + fout_name, 'w') as fout:
        for name_to_check in names_to_check:
            try:
                correct_name = check_trader_name(name_to_check, names_dict)
                fout.write(correct_name + '\n')
            except TypeError:
                fout.write('\n')
