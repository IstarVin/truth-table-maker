import copy
from itertools import product

from prettytable import PrettyTable


def letter_truth_values(num):
    values_combinations = product(['T', 'F'], repeat=num)

    return [x for x in values_combinations]


def get_negation(proposition: str):
    return list(set([f"~{char}" for i, char in enumerate(proposition)
                     if char.isalpha() and i != 0 and proposition[i - 1] == '~']))


def get_parenthesis(proposition: str):
    par_list = []

    parenthesis_index_list = [[i, char] for i, char in enumerate(proposition) if char in '()']

    while True:
        should_break = True
        for i, par in enumerate(parenthesis_index_list):
            if i == len(parenthesis_index_list) - 1:
                break

            cur = par
            before_proposition = '' if cur[0] == 0 else proposition[cur[0] - 1]
            after = parenthesis_index_list[i + 1]
            if cur[1] == '(' and after[1] == ')':
                parenthesis_index_list.pop(i)
                parenthesis_index_list.pop(i)
                par_list.append(proposition[cur[0] + 1:after[0]])
                should_break = False

            if before_proposition == '~' and cur[1] == '(' and after[1] == ')':
                par_list.append('~' + proposition[cur[0]:after[0] + 1])

        if should_break:
            break

    return par_list


def main():
    # proposition = input('Enter a proposition (ex. "(pv(q^s))^(~rvs)"): ')
    proposition = '(~pv(q^s))^~(~rv(sv~p))'
    letters = list(set([x for x in proposition if x.isalpha() and x != 'v']))
    letters.sort()

    truth_table_head = []
    truth_table_head.extend(letters)
    truth_table_head.extend(get_negation(proposition))
    truth_table_head.extend(get_parenthesis(proposition))
    truth_table_head.append(proposition)

    truth_table = PrettyTable(truth_table_head)

    expressions = truth_table_head[len(letters):]

    for i in letter_truth_values(len(letters)):
        truth_table_row = [x for x in i]

        per_letter_truth = {letter: 'T' if truth_value == 'T' else 'F' for letter, truth_value in
                            zip(letters, truth_table_row)}

        # translate_table = str.maketrans(''.join(letters), ''.join(['1' if char == 'T' else '0' for char in i]))

        for x in expressions:
            # print(x.translate(translate_table))

            expression = copy.deepcopy(x)
            #
            # for j, char in enumerate(x):
            #     if char in letters and j != len(x) - 1 and (not x[j + 1].isalpha() or x[j + 1] == 'v'):
            #         expression = expression[:j] + per_letter_truth[char] + expression[j + 1:]

            for key, value in per_letter_truth.items():
                x = x.replace(key, '1' if value == 'T' else '0')

            x = x.replace("~", "not ").replace("v", " or ").replace("^", " and ")

            eval_res = eval(x)

            # print(eval_res, x)

            result = 'T' if eval_res != 0 else 'F'

            truth_table_row.append(result)

        truth_table.add_row(truth_table_row)

    print(truth_table)


if __name__ == '__main__':
    main()
