# Dificuldades Encontradas

## Uma Montanha-Russa

### Abordagem 1

Uma dificuldade encontrada durante a abordagem 1 foi dividir e separar os diferentes estados e condições das threads/objetos/rotinas/programa para fazer de fato a sincronização entre as threads. Como por exemplo, os estados de cheio, vazio, em embarque e em desembarque. E fazer com que os passageiros esperem os estados embarque e desembarque para poderem fazer as ações de entrar e sair do carro, respctivamente.

### Abordagem 2

Uma dificuldade foi usar barreiras para controlar a entrada de passageiros. No versão final, as barreiras foram utilizadas apenas para controlar a saída dos passageiros do carro mesmo.

### Extra 1

##### Abordagem 1

Uma dificuldade durante a implementação da abordagem 1 do extra foi a questão de gerenciar a fila dos carros e fazer com que as pessoas entrem corretamente no carro atual da plataforma.

A questão de gerenciar a fila dos carros foi resolvido com a implementação de uma fila sequencial, onde a fila só prossegue quando o carro atual inicie seu passeio.  
Enquanto a questão das pessoas entragem corretamente no carro atual foi resolvido com a ajuda da fila sequencial dos carros e ter um carro atual da plataforma que muda, fazendo com que os passageiros só tentem alocar o assento do carro correto.

##### Abordagem 2

### Extra 2

Uma dificuldade encontrada foi usar locks e variáveis condicionais para controlar a chegada em ordem dos carros. Na versão final utilizou-se semáforos nessa parte. Para usar locks, uma possível abordagem seria a utilização de uma fila para controlar a chegada dos carros na "plataforma de desembarque".

## Banheiro Unissex

### Abordagem 1

Uma dificuldade durante a implementação da abordagem 1, foi que as pessoas de um sexo 'X' entravam em starvation caso o tempo de "trabalho" e a quantidade de trabalhadores fossem muito superior à quantidade de vagas do banheiro. E não era garantido que uma pessoa da fila realmente entrasse no banheiro em algum momento, pois todas as pessoas do mesmo sexo eram liberadas ao mesmo tempo para adquirir a vaga, ficando assim em starvation.

As soluções para esses dois tipos de starvation foram, respectivamente:

1. Implementação de um método de justiça para o gênero do banheiro
2. Implementação de uma fila sequencial para as pessoas respeitarem uma ordem

Com isso garantindo a execução sem starvation.

### Abordagem 2

A dificuldade maior foi controlar a troca de sexo do banheiro evitando livelocks e que alguém do outro gênero entrasse. Erros muito provavelmente ocasionados por motivos de exaustão

