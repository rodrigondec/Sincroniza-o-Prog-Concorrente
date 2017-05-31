# Extra Uma Montanha-Russa

## Descrição do problema

Desenvolva uma segunda versão do programa para fazer com que a montanha-russa comporte múltiplos carros. Essa segunda versão não é uma simples generalização da anterior em que tem-se agora  m carros de igual capacidade C \(ao invés de apenas um\), mas também satisfaz o seguinte conjunto de restrições adicionais:

* o embarque de passageiros só pode ser feito em um carro por vez;
* os múltiplos carros podem estar simultaneamente na trilha;

* uma vez que um carro não pode ultrapassar outro na trilha, o desembarque de passageiros tem de  
   ser feita na mesma ordem em que eles embarcaram;

* os passageiros de um carro só podem desembarcar dele quando todos os passageiros do carro que  
   está a sua frente já tenham saído.

## Análise do problema

O problema consiste em algumas pontos a serem satisfeitos, tais como:

1. Os vários carros respeitarem uma ordem de fila
2. Apenas um carro estar em processo de embarque/desembarque
3. Os passageiros entrarem/saírem apenas no/do carro que está em processo de embarque/desembarque
4. Todos os pontos originais do problema [Uma Montanha-Russa](/Documents/2-uma-montanha-russa.md)

As sincronizações necessárias entre as partes do programa, são entre as etapas de embarque, passeio, desembarque, limite de vagas do carro, ordem dos carros e fila de passageiros. Tendo em mente isso implementaremos soluções utilizando metodologias/tecnologias com o intuito de garantir a corretude entre esses quesitos.

