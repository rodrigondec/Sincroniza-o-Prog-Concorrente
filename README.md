# Projeto 2ª unidade de Programação Concorrente
## Índice
- [Executando](#executando)
- [Problemas](#problemas)
    - [Uma Montanha Russa](#uma-montanha-russa)
        - [Abordagem 1](#abordagem-1)
            - [Sincronização](#sincronização)
            - [Classes](#classes)
                - [Carro](#carro)
                - [Passageiro](#passageiro)
        
## Executando
Para executar os programas criados, executar o comando `python <problema>/<abordagem>/<nome>.py`. Onde `<problema>` é o nome do problema, `<abordagem>` é a abordagem a ser rodada e `<nome>` é o nome do arquivo. Por exemplo: `python montanha-russa/abordagem_1/montanha.py`

## Problemas
Nesse projeto são encontrados dois problemas:
- Uma Montanha-Russa
- O Banheiro Unissex

Para mais informações leia [Trabalho-Sincronizacao.pdf](https://github.com/rodrigondec/Sincronizacao-Prog-Concorrente/blob/master/Trabalho-Sincronizao.pdf)

### Uma Montanha-Russa
#### Abordagem 1
##### Sincronização
A solução desse problema foi baseada em variáveis de condição. 
Mais especificamente utilizando `Event` objects da biblioteca `threading` do python3. 

Esse objeto possiu um status `True` ou `False` e um método `wait()` que bloqueia o processo que chamar esse método caso o status seja `false`. 
Dessa forma podemos verificar se a condição se foi satisfeita ou esperar até que ela seja satisfeita.

##### Classes
Temos duas classes para resolver o problema:
- Carro
- Passageiro

###### Carro
Atributos:
- limite_pessoas: quantidade de pessoas que cabem no carro
- num_passeios: número de vezes que o carro irá rodar
- passageiros: lista de passageiros no carro
- thread_main: Thread principal do carro com todos os estágios
- thread_run: Thread representando o passeio do carro nos trilhos

Atributos situação:
- boardable: Event - representando o estágio de embarque do carro
- unboardable: Event - representando o estágio de desembarque do carro
- cheio: Event - representando o status lotado do carro
- vazio: Event - representando o status vazio do carro

Métodos:
- main: método controlador do carro
- run: método de passeio do carro
- load: método que libera o embarque no carro
- unload: método que libera o desembarque no carro
- board: método para adicionar um passageiro no carro
- unboard: método para remover um passageiro no carro

Condições:
- Para o embarque do carro ser liberado é necessário que o carro esteja vazio
- Para que o carro esteja na situação `boardable` é necessário que ele não esteja cheio
- Para que o passeio do carro seja iniciado é necessário que o carro esteja cheio
- Para que o desembarque do carro seja liberado é necessário que o passeio tenha terminado
- Para que o carro continue na situação `unboardable` é necessário que ele não esteja vazio

###### Passageiro
Atributos:
- id_passageiro: identificador do passageiro
- thread: thread que representa a vida do passageiro no parque de diversões

Métodos:
- run: método que representa a vida do passageiro no parque de diversões
- passear: método para o passageiro passear pelo parque de diversões
- board: método para o passageiro embarcar no carro da montanha russa
- unboard: método para o passageiro desembarcar no carro da montanha russa

Condições:
- Para um passageiro embarcar num carro, o carro precisa estar na situação `boardable`
- Para um passageiro desembarcar de um carro, o caro precisa estar na situação `unboardable`
