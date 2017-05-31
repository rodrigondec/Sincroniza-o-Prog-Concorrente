# Dificuldades Encontradas

## Uma Montanha-Russa

### Abordagem 1

Uma dificuldade encontrada foi dividir e separar os diferentes estados e condições das threads/objetos/rotinas/programa para fazer de fato a sincronização entre as threads. Como por exemplo a modelagem da montanha-russa, na qual os passageiros entrarem/saírem do carro em determinados estados do carro.

### Abordagem 2

bla

### Extra

##### Abordagem 1

Uma dificuldade durante a implementação da abordagem 1 do extra foi a questão de gerenciar a fila dos carros e fazer com que as pessoas entrem corretamente no 'carro atual' da plataforma. 

A questão de gerenciar a fila dos carros foi resolvido com a implementação de

##### Abordagem 2

## Banheiro Unissex

### Abordagem 1

Uma dificuldade durante a implementação da abordagem 1, foi que as pessoas de um sexo 'X' entravam em starvation caso o tempo de "trabalho" e a quantidade de trabalhadores fossem muito superior à quantidade de vagas do banheiro. E não era garantido que uma pessoa da fila realmente entrasse no banheiro em algum momento, pois todas as pessoas do mesmo sexo eram liberadas ao mesmo tempo para adquirir a vaga, ficando assim em starvation.

As soluções para esses dois tipos de starvation foram, respectivamente:

1. Implementação de um método de justiça para o gênero do banheiro
2. Implementação de uma fila sequencial para as pessoas respeitarem uma ordem

Com isso garantindo a execução sem starvation.

### Abordagem 2

bla

