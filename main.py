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
    # proposition = input('Enter a proposition (ex. "(pv(q<=>s))^(~r+s)"): ')
    proposition = 'p=>q'
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

        for x in expressions:
            result = 'T'

            for key, value in per_letter_truth.items():
                x = x.replace(key, '1' if value == 'T' else '0')

            if '=>' in x and '<=>' not in x:
                x_split = x.split('=>')

                if eval(x_split[0]) and not eval(x_split[1]):
                    result = 'F'

            else:
                x = x.replace("~", "not ").replace("v", " or ").replace("^", " and ")
                x = x.replace('<=>', '==').replace('+', '!=')
                eval_res = eval(x)

                result = 'T' if eval_res != 0 else 'F'

            truth_table_row.append(result)

        truth_table.add_row(truth_table_row)

    print(truth_table)


if __name__ == '__main__':
    main()
