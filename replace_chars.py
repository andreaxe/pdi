import os

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

    # xml_str = ET.tostring(xml).decode()
    # print(xml_str)
    # print(contents)
    # myStrLen = len(contents)
    # print(myStrLen)

    # with open(os.path.join('adchecker_results', 'cnpcjr.pt.xml'), 'w') as file:
    #     # data = file.read().replace('\n', '')
    #     data = file.read()
    #     print(data)
