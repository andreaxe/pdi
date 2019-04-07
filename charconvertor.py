import os


def extract_key_value_to_dict(filename):

    all_lines = open(filename, 'r').readlines()
    dictionary = {}
    for line in all_lines:
        key,value=line.split(':')
        dictionary[key] = value.strip()

    return dictionary


def string_to_convert(string):

    htmlspecialchar = extract_key_value_to_dict("spcharhtml")
    for k,v in htmlspecialchar.items():
        if string.find(v) != -1:
            print(string.replace(v, k))


if __name__ == '__main__':

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
