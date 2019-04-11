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



### Considerações finais:

* Foram cumpridas todos os requisitos propostos contudo apenas há um aspecto que não foi possivel melhorar (conforme detectado na apresentação prévia) que tem a ver com o redireccionamento automático em situações em que o servidor socket se encontra indisponivel.
Foi possivel minimizar erros que poderiam surgir ao utilizador contudo não foi possivel em tempo útil melhorar muito mais nesse aspecto.

* A aplicação cliente após autenticação correcta no servidor de sockets, regista uma sessão que permite navegar por entre as páginas autenticado e efectuar pedidos ao servidor socket. Contudo em caso de anomalia no servidor socket o comportamento não é o ideal (vai de encontro à problemática do ponto anterior).

* Quantos aos aspectos positivos, a aplicação foi desenhada tendo em consideração uma interface responsive ideal para se adaptar a qualquer dispositivo (desktop, mobile). Todos os aspectos funcionais do site funcionam de acordo com o proposto e não se detectou anomalias durante a navegação, provando-se consistente. 
 

Exemplos:
=========

**./ConnectDB.php (Conexão à base de dados)**

Alterar as variáveis de classe existentes neste ficheiro para se conectar à sua base de dados.

    class ConnectDB{
        /**
         * @var bool|mysqli
         * Alterar aqui as credenciais de acesso à Base de dados
         */
    
        public $db_connection = false;
        public $logs = array();
        private $_servername = "172.17.0.1"; // alterar
        private $_username = "andre"; // alterar
        private $_password = "andre"; // alterar
        private static $_instance;
        private $_database = 'cvp'; // alterar SE o nome da BD for diferente

**./server.php (Servidor)**

Caso seja necessário alterar a porta usada pelo socket deverá alterar a váriável $port

    <?php    
    $port = 8000;

**./lib/socketClient.class.php (Cliente)**

No caso do cliente deverá alterar no constructor da classe *socketClient*

    Class socketClient extends socket{
    
        private $connected = True;
    
    	function __construct($ip = "127.0.0.1", $port = 8000, $auth = false){
    		parent::__construct($ip, $port, $auth);
    	}
    	

Exemplo de criação um array com a informação da classe, método e argumentos a serem executados pelo servidor:

    <?php
    require('./lib/socket.class.php');
    require('./lib/socketClient.class.php');
    
    $socket = new socketClient('127.0.0.1', 8000);
    
    $packet = array('controller' => 'index', 'action' => 'login', 
                    'args' => ['email'=> $_POST['email'], 'pass' => $_POST['password']]);
    $results = json_decode($socket->send(json_encode($packet)));
    
    $response = $socket->send(json_encode($packet));
        
    ?>

Servidor
------------------

**./server.php (Server)**
    
       <?php
       
       // Funcão que encaminha o pedido para o controlador respectivo
       function run_controller($route){
           /* create controllers class instance & inject core */
           $controller = './lib/serverControllers/'.$route->controller.'Controller.php';
           if(file_exists($controller)) {
               require_once($controller);
               $class = $route->controller.'Controller';
               if(class_exists($class)) {
                   $controller = new $class($route);
               }
           } else {
               require_once('./lib/serverControllers/not_foundController.php');
               $controller = new not_foundController();
           }
           /* check the root class is callable */
           if (is_callable(array($controller, $route->action)) === false) {
               /* index() method because not found method */
               $action = 'index';
           } else {
               /* action() method is callable */
               $action = $route->action;
           }
           /* run the action method */
           return $controller->{$action}();
       }
       
       // Socket server começa aqui
       set_time_limit (0);
       // Set the ip and port we will listen on
       $address = '127.0.0.1';
       $port = 8000;
       // Create a TCP Stream socket
       $sock = socket_create(AF_INET, SOCK_STREAM, 0); // 0 for  SQL_TCP
       // Bind the socket to an address/port
       socket_bind($sock, 0, $port) or die('Could not bind to address');  //0 for localhost
       // Start listening for connections
       socket_listen($sock);
       //loop and listen
       
       while (true) {
           /* Accept incoming  requests and handle them as child processes */
           $client =  socket_accept($sock);
           // Read the input  from the client – 1024000 bytes
           $input =  socket_read($client, 1024000);
           $output =  json_decode($input);
       
           $response = run_controller($output);
           /* run the action method */
           // Display output  back to client
           socket_write($client, $response);
           socket_close($client);
       }
       // Close the master sockets
       socket_close($sock);
       ?>

Interface gráfica
===================

![image](https://user-images.githubusercontent.com/9929973/51805947-9c431d80-226b-11e9-9b21-0f8cfe9067a3.png)

![image](https://user-images.githubusercontent.com/9929973/52072278-9e172480-257c-11e9-9812-2a8dcdc06da5.png)

![image](https://user-images.githubusercontent.com/9929973/52072418-dae31b80-257c-11e9-91c1-779af1b3ea32.png)

