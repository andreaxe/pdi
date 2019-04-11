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
    fig, ax = plt.subplots()

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, legenda,  frameon=False, loc='lower left')
    # ax.legend(wedges, legenda,
    #           title=titulo,
    #           loc='upper left')

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title(titulo)
    fig.savefig('{}.eps'.format(titulo), format='eps')
    plt.show()


def element_of_interest(argument):

    elements_required = ['status', 'NumOfErrors', 'NumOfLikelyProblems', 'NumOfPotentialProblems']
    if argument in elements_required:
        return True
    return False


def xml_to_pandas(errors=50, potencial_problems=10, likely_problems=10):

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
    df.to_csv('resultado_analise.csv')
    print(len(errors))

    df['NumOfErrors'] = pd.to_numeric(df['NumOfErrors'])
    df['NumOfPotentialProblems'] = pd.to_numeric(df['NumOfPotentialProblems'])
    df['NumOfLikelyProblems'] = pd.to_numeric(df['NumOfLikelyProblems'])
    websites_passed = df[df['status'] == 'PASS'].count().website
    websites_failed = df[df['status'] == 'FAIL'].count().website
    websites_conditional = df[df['status'] == 'CONDITIONAL PASS'].count().website
    plot_donut([websites_passed, websites_conditional, websites_failed], ['Positivos', 'Positivos Condicionais',
                                                                          'Negativos'], "WCGA 2.0 - Avaliação")

    print("Websites passed: {} ".format(df[df['status'] == 'PASS'].count().website))
    print("Websites failed: {}".format(df[df['status'] == 'FAIL'].count().website))

    only_errors = df[df['NumOfErrors'] > 0]

    stat_errors = only_errors[only_errors['NumOfErrors'] < num_of_errors].count().website
    inv_stat_errors = only_errors[only_errors['NumOfErrors'] >= num_of_errors].count().website

    print("Websites with number of errors lower than {}: {}".
          format(num_of_errors, stat_errors))

    stat_likely_errors = only_errors[only_errors['NumOfLikelyProblems'] < num_of_likely_problems].count().website
    inv_stat_likely_errors = only_errors[only_errors['NumOfLikelyProblems'] >= num_of_likely_problems].count().website
    print("Websites with number of NumOfLikelyProblems lower than {}: {}".
          format(num_of_likely_problems, stat_likely_errors))

    stat_potencial_errors = only_errors[only_errors['NumOfPotentialProblems'] < num_of_potencial_problems].count().website
    inv_stat_potencial_errors = only_errors[only_errors['NumOfPotentialProblems'] >= num_of_potencial_problems].count().website

    print("Websites with number of Potential Problems errors lower than {}: {}"
          .format(num_of_potencial_problems, stat_potencial_errors))

    plot_donut([stat_errors, inv_stat_errors], ['erros < {}'.format(num_of_errors), 'erros > {}'.format(num_of_errors) ],
               "WCGA 2.0 - Avaliação de erros")

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

    # ================ Lista de 10 websites com o maior número de erros ================ #

    df = df.sort_values('NumOfErrors', ascending=False).head(10)
    df['website'] = df['website'].str.replace('.xml', '')
    plot = df.plot(x="website", y=['NumOfErrors', 'NumOfPotentialProblems', 'NumOfLikelyProblems'], kind="bar", rot=75,
                   fontsize=10)

    fig = plot.get_figure()

    fig.savefig('analise_plot.svg', dpi=1200, bbox_inches="tight")

    plt.show()


    # print("Websites with number of potencial errors greater than {}:".format(num_of_potencial_problems))
    # df[df['NumOfPotentialProblems'] < 2].count().website))
    # print("Sites OK: " + df[df['status'] == 'PASS'].count())


# xml_to_pandas()
