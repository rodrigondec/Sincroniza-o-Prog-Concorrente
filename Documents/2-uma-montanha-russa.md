# Uma Montanha-Russa

## Descrição do problema

> Uma montanha-russa é uma atração popular dos parques de diversão e parques temáticos modernos, consistindo de uma estrutura de aço formando uma trilha composta por elevações seguidas de quedas e por vezes inversões. A maioria das montanhas-russa tem vários carros em que os passageiros sentam-se e são contidos \(obviamente por questões de segurança\), enquanto que algumas funcionam com um carro único e um número maior de passageiros.



> Suponha uma montanha-russa contendo um único carro com capacidade para C passageiros. Os passageiros, em um total de n \(n &gt; C\), frequentemente esperam para entrar no carro, que só pode ser liberado para a trilha quando está cheio. Após terminar um passeio, cada passageiro continua passeando pelo parque de diversões antes de retornar à montanha-russa para tentar novamente entrar no brinquedo em um outro passeio. Por questões de segurança, o carro realiza apenas P passeios por dia e, uma vez alcançado esse número, é desligado.



> Projete e implemente programa que simule a operação da montanha-russa satisfazendo os seguintes requisitos:
>
> * o carro permite a entrada de exatamente C passageiros;
> * nenhum passageiro pode entrar no carro enquanto ele estiver em movimento sobre a trilha;
>
> * nenhum passageiro pode pular do carro enquanto ele estiver em movimento sobre a trilha;
>
> * nenhum passageiro poderá entrar novamente no carro sem que primeiro saia dele.



> Durante a execução do programa, as seguintes ações devem ser realizadas para cada entidade:
>
> * as ações realizadas por passageiros são o embarque \(board\) e o desembarque \(unboard\) do carro;
>
> * o carro permite a entrada \(load\) e saída \(unload\) de passageiros;
>
> * o movimento do carro é iniciado pela execução da operação run;
>
> * os passageiros não podem entrar no carro até que a operação load seja executada pelo carro;
>
> * o carro não pode iniciar seu movimento até que todos os C passageiros tenham entrado;
>
> * os passageiros não podem sair do carro até que a operação unload seja executada pelo carro.
>
> * o tempo em que cada passageiro passeia pelo parque antes de ir novamente à montanha-russa é  
>    randômico e diferente a cada execução do programa.

## Análise do problema

O problema consiste em algumas pontos a serem satisfeitos, tais como:

1. O embarque ser liberado apenas quando não há mais passageiros no carro
2. Passageiros entrarem no carro só depois de o embarque ser liberado
3. O carro só fazer o trajeto da montanha russa após ele estar lotado
   1. O passeio do carro é por um tempo randômico
4. O desembarque só pode ser liberado depois que o passeio do carro acabar
   1. Após o desembarque, os passageiros passeiam pelo parque por um tempo randômico
5. O carro irá fazer um novo passeio, recomeçando do passo 1, n vezes

  
As sincronizações necessárias entre as partes do programa, são entre as etapas de embarque, passeio, desembarque e limite de vagas do carro. Tendo em mente isso implementaremos soluções utilizando metodologias/tecnologias com o intuito de garantir a corretude entre esses quesitos.





