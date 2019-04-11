import os


def extract_key_value_to_dict(filename):
    all_lines = open(filename, 'r').readlines()
    dictionary = {}
    for line in all_lines:
        key, value = line.split(':')
        dictionary[key] = value.strip()

    return dictionary


def string_to_convert(string):
    htmlspecialchar = extract_key_value_to_dict("spcharhtml")
    for k, v in htmlspecialchar.items():
        if string.find(v) != -1:
            print(string.replace(v, k))


def crawl():
    from crawler import crawl_web

    limite = input("Inserir número máximo de sites a pesquisar: ")
    webpage = 'https://www.eapn.pt/links/governo-da-republica-portuguesa-e-instituicoes-publicas'
    crawl_web(webpage, limit=limite)


def my_quit_fn():
    raise SystemExit


def analise():

    from analysis import xml_to_pandas
    xml_to_pandas()
    menu()


def parse_results():

    files = os.listdir(os.path.join('adchecker_results'))

    for xml in files:
        print("Cleaning file: " + xml)
        xml_content = open(os.path.join('adchecker_results', xml)).read()

        with open('chars', 'r') as f:
            words = [line.strip() for line in f]

        for word in words:
            xml_content = xml_content.replace(word, "")

        f = open(os.path.join('results', xml), 'wt', encoding='utf-8')
        f.write(xml_content)

    menu()


def _sep():
    print("===========================================")


def _empty():
    print("")


def _clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def avaliacao():

    from evaluation import evaluate_websites
    answer = None
    if os.path.exists('crawler_results.txt'):
        while answer not in ("s", "n"):
            answer = input("Pretende usar o ficheiro que resultou do Crawler? (yes/no) ")
            if answer == "yes":
                evaluate_websites()
                break
            elif answer == "no":
                evaluate_websites(file='sites_list.txt')
                break
            else:
                print("Please enter yes or no.")
    else:
        evaluate_websites(file='sites_list.txt')
    menu()


def reset():

    files = ['resultado_analise.csv', 'WCGA 2.0 - Avaliação.eps', 'WCGA 2.0 - Avaliação.eps', 'crawler_results.txt',
             'analise_plot.svg']

    for file in files:
        if os.path.isfile(file):
            os.remove(file)

    import shutil
    adchecker_directory = 'adchecker_results'
    results = 'results'
    if os.path.exists(adchecker_directory):
        shutil.rmtree(adchecker_directory)
    if os.path.exists(results):
        shutil.rmtree(results)

    os.makedirs(adchecker_directory)
    os.makedirs(results)

    menu()


def menu():

    _clear_console()
    ok = '\033[92m' + 'OK' + '\033[0m'
    not_ok = '\033[91m' + 'NOT OK' + '\033[0m'

    choice = '0'
    crawl_file = '\033[91m' + 'NOT OK' + '\033[0m'
    results_parsed = ok if os.listdir('results') else not_ok
    results_ready = ok if os.listdir('adchecker_results') else not_ok

    if os.path.isfile('crawler_results.txt'):
        crawl_file = '\033[92m' + 'OK' + '\033[0m'

    while choice == '0':
        _clear_console()

        print("     MAIN MENU")
        print("1  - Efectuar crawl de endereços: " + '\033[1m' + crawl_file + '\033[0m')
        print("2  - Efectuar a avaliação dos endereços: " + '\033[1m' + results_ready + '\033[0m')
        print("3  - Efectuar o parse dos resultados: " + '\033[1m' + results_parsed + '\033[0m')
        print("4  - Executar análise de resultados: ")
        _sep()
        print("9  - Reset ao programa ")
        print("10 - Exit")
        _empty()
        choice = input("Please make a choice:")

        if choice == "1":
            crawl()
        elif choice == "2":
            avaliacao()
        elif choice == "3":
            parse_results()
        elif choice == "4":
            if os.listdir('results'):
                analise()
            else:
                print("A pasta resultados encontra-se vazia. Necessita de efectuar o parse dos resultados.")
        elif choice == "9":
            reset()
        elif choice == "10":
            exit("Programa terminado.")
        else:
            print("A resposta não é válida")


if __name__ == '__main__':

    menu()

