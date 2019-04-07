import os
import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import numpy as np
import matplotlib.pyplot as plt


def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)


def plot_donut(data, legenda, titulo):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))
    ax.legend(wedges, legenda,
              title="WCGA 2",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title(titulo)

    plt.show()


def element_of_interest(argument):

    elements_required = ['status', 'NumOfErrors', 'NumOfLikelyProblems', 'NumOfPotentialProblems']
    if argument in elements_required:
        return True
    return False


def xml_to_pandas(errors=10, potencial_problems=10, likely_problems=10):

    num_of_errors = errors
    num_of_potencial_problems = potencial_problems
    num_of_likely_problems = likely_problems

    data = {'website': [], 'status': [], 'NumOfErrors': [], 'NumOfLikelyProblems': [], 'NumOfPotentialProblems': []}
    errors = []
    directory = 'results'
    xml_files = os.listdir(os.path.join(directory))

    for file in xml_files:

        file = os.path.join(directory, file)
        try:
            e = ET.ElementTree(ET.parse(file))
        except ParseError as e:
            print("Erro {} a processar o ficheiro: {}".format(repr(e), file))
            errors.append(file)
            continue

        for elt in e.iter():
            if element_of_interest(elt.tag):
                data[elt.tag].append(elt.text)

        data['website'].append(file[8:])

    df = pd.DataFrame(data)
    df['NumOfErrors'] = pd.to_numeric(df['NumOfErrors'])
    df['NumOfLikelyProblems'] = pd.to_numeric(df['NumOfLikelyProblems'])
    df['NumOfPotentialProblems'] = pd.to_numeric(df['NumOfPotentialProblems'])

    # df.sort_values(by=['NumOfErrors'], inplace=True)
    print(df.head())
    print(df.to_csv('teste.csv'))
    print(len(errors))

    df['NumOfErrors'] = pd.to_numeric(df['NumOfErrors'])
    df['NumOfPotentialProblems'] = pd.to_numeric(df['NumOfPotentialProblems'])
    df['NumOfLikelyProblems'] = pd.to_numeric(df['NumOfLikelyProblems'])
    websites_passed = df[df['status'] == 'PASS'].count().website
    websites_failed = df[df['status'] == 'FAIL'].count().website
    plot_donut([websites_passed, websites_failed], ['WCGA compativel', 'WCGA não compativel'], "WCGA - Resultado")

    print("Websites passed: {} ".format(df[df['status'] == 'PASS'].count().website))
    print("Websites failed: {}".format(df[df['status'] == 'FAIL'].count().website))

    stat_errors = df[df['NumOfErrors'] > num_of_errors].count().website

    print("Websites with number of errors greater than {}: {}".
          format(num_of_errors, stat_errors))

    stat_likely_errors = df[df['NumOfLikelyProblems'] > num_of_likely_problems].count().website
    print("Websites with number of NumOfLikelyProblems greater than {}: {}".
          format(num_of_likely_problems, stat_likely_errors))

    stat_potencial_errors = df[df['NumOfPotentialProblems'] > num_of_potencial_problems].count().website
    print("Websites with number of Potential Problems errors greater than {}: {}"
          .format(num_of_potencial_problems,stat_potencial_errors ))

    plot_donut([stat_errors, stat_likely_errors, stat_potencial_errors],
               ['errors > {}'.format(num_of_errors), 'likely errors > {}'.format(num_of_likely_problems),
                'potencial_errors > {}'.format(potencial_problems)], "WCGA - Tipos de erro")

    # ================ Website com o maior número de erros ================ #

    print(df.loc[df['NumOfErrors'].idxmax()])
    high_errors = df.loc[df['NumOfErrors'].idxmax()]
    high_pontencial_errors = df.loc[df['NumOfPotentialProblems'].idxmax()]
    high_likely_errors = df.loc[df['NumOfLikelyProblems'].idxmax()]

    print("Website com o maior número de erros: {} : {}".format(high_errors.website, high_errors.NumOfErrors))
    print("Website com o maior número de erros potenciais: {} : {}".format(high_pontencial_errors.website,
                                                                           high_pontencial_errors.NumOfPotentialProblems))
    print("Website com o maior número de erros potenciais: {} : {}".format(high_likely_errors.website,
                                                                           high_likely_errors.NumOfLikelyProblems))



    exit()
    # print("Websites with number of potencial errors greater than {}:".format(num_of_potencial_problems))
    # df[df['NumOfPotentialProblems'] < 2].count().website))
    # print("Sites OK: " + df[df['status'] == 'PASS'].count())


xml_to_pandas()
