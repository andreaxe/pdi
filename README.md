Trabalho de PDI
============================
	
Tema:

Pretende-se identificar os sítios Web do governo português e classifica-los no que concerne ao cumprimento dos padrões 
WCAG2 (https://www.w3.org/WAI/WCAG21/quickref/).
Para este trabalho, os sítios Web a considerar: (i) deverão ter como domínio de topo .gov.pt; (ii) ou ter alguma 
referência textual que os identifique como pertencendo a uma reguladora ou a um entidade concessionada pelo governo 
português. Os sítios Web dos municípios/autarquias ficam excluídos deste trabalho.

O trabalho contempla três componentes: (i) inventariação dos sítios Web; (ii) classificação do padrão de acessibilidade
 (avaliar apenas a página inicial); (iii) elaboração do relatório técnico.
  
Os objetivos a atingir com o trabalho são: (i) selecionar e recolher a informação alvo e previamente e objetivamente 
identificada; (ii) identificar e recolher a informação alvo, subjetiva e sujeita a julgamento humano; (iii) utilizar 
 e(ou) desenvolver técnicas manuais ou automatizadas para identificação, recolha e seleção de informação.


Objectivo e instruções para deploy do projecto
============

A aplicação deverá ser capaz de sondar dominios com a designação .pt e .gov a partir de um dominio pré-designado.
Após a recolha dos dominios alvo deverá ser capaz de comunicar com uma aplicação terceira (Achecker) e avaliar
esses mesmos dominios segundo as recomendações da norma WCAG21.

Para colocar a funcionar este projecto é necessário o seguinte:
 
* Python 3.6 instalado; https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe
* biblioteca *beautifulsoup4==4.7.1*
* biblioteca *pandas==0.24.2*

Através da linha de comandos instalar as seguintes bibliotecas:

* pip install beautifulsoup4==4.7.1
* pip install pandas==0.24.2

Correr o programa (posicionar-se no directório do programa):

* python main.py

![image](https://user-images.githubusercontent.com/9929973/55993432-008c4f80-5ca7-11e9-91d9-59395b692096.png)

### Notas

* De preferência deverá seguir os pontos pela ordem apresentada no menu.
* Efectuar **RESET** ao programa é uma boa forma de iniciar uma nova avaliação.
* Se preferir não efectuar a avaliação aos sites recolhidos, por defeito a aplicação fará a avaliação aos endereços
que constam no ficheiro *sites_list.txt* 


