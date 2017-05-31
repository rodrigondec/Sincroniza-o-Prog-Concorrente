# Abordagem 2

## Descrição

Essa abordagem utiliza [Locks](https://docs.python.org/3/library/threading.html#lock-objects), [Variáveis Condicionais](https://docs.python.org/3/library/threading.html#condition-objects) e [Barreiras](https://docs.python.org/3/library/threading.html#barrier-objects): objetos disponibilizados pela biblioteca threading de python 3. Quanto à estrutura de dados, uma "fila" é utilizada \(na realidade apenas a lista padrão de python é utilizada, mas os métodos chamados simulam o comportamento de uma fila\).

Na simulação, cada passageiro corresponde à uma thread, bem como o carro. Há uma fila de entrada para evitar starvation das threads de passageiros \(enquanto esperam entrar no carro\). Os locks estão sendo utilizados para garantir exclusão mútua e consistência, i.e. operações de inserção e remoção nas listas. As variáveis condicionais estão sendo utilizadas para economozar tempo e processamento desnecessário; por exemplo, quando um passageiro tem que esperar ser o primeiro da fila para poder entrar no carro. Por último, a barreira é utilizada para liberar a saída dos passageiros dos carros, como se fosse uma variável condicional compartilhada.

Deadlocks e livelocks foram evitados, basicamente, adquirindo-se locks em ordem e garantindo que variáveis condicionais só seriam notificadas caso estivessem esperando.

## Classes

* [Carro](#carro)
* [Passageiro](#passageiro)

### Carro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| limite\_pessoas | Armazena a capacidade máxima de pessoas que o carro comporta | inteiro |
| num\_passeios | Armazena a quantidade de passeios que o carro deve realizar ao todo antes de ir dormir | inteiro |
| passageiros | Uma lista que armazena todos os passageiros que estão dentro no carro num dado momento. A quantidade de objetos na fila nunca é superior ao limite\_pessoas | Lista de [Passageiro](#passageiro) |
| fila | Armazena as pessoas esperando para entrar no carro | Lista de [Passageiro](#passageiro) |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| barr | Utilizado para impedir que passageiros "pulem" da montanha-russa. É utilizado para liberar os passageiros para desembarque | [Barrier](https://docs.python.org/3/library/threading.html#barrier-objects) |
| lk | Utilizado para garantia exclusão mútua e garantir consistência ao realizar operações de adição e remoção em passageiros e/ou fila | \[Lock\]\(\([https://docs.python.org/3/library/threading.html\#lock-objects](https://docs.python.org/3/library/threading.html#lock-objects)\)\) |
| cv\_car | Utilizado para fazer a thread do carro dormir e esperar que uma condição aconteça para que volte a agir \(carro ficar cheio ou vazio\). Evita processamento desnecessário. | [Condition](https://docs.python.org/3/library/threading.html#condition-objects) |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| main | Simula o comportamento de um carro da montanha russa. Executa o ciclo de vida num\_passeio vezes |
| run | Simula o carro andando na montanha-russa. Thread dorme por um tempo |
| load | Operação que permite que passageiros entrem no carro. Acorda exatamente limite\_pessoas threads que estejam esperando na fila para que elas entrem no carro. Caso não haja pessoas suficientes na fila, espera alguém entrar nela através do método entrar\_fila |
| unload | Autoriza o desembarque. Thread chama barr.wait\(\), acordando todos os passageiros dentro do carro. Thread dorme enquanto houver passageiros no carro |
| board | Operação chamada pelo passageiro. Adiciona passageiro no carro e o notifica \(cv\_car\) para que possa verificar se está cheio. O lock lk deve ter sido adquirido previamente |
| unboard | Operação chamada pelo passageiro. Remove o passageiro do carro e o notifica \(cv\_car\) caso esteja vazio. |
| entrar\_fila | Adquire lock lk para adicionar passageiro na fila de espera. Após adicionar, notifica o carro que pode estar esperando por passageiros para ficar cheio |

#### Condições e fluxo

##### Carro

1. O carro libera o embarque, acordando passageiros na fila. Adquire lk e dorme \(cv\_car\) enquanto não estiver cheio
2. O carro está cheio e anda na montanha russa \(dorme por um determinado tempo\)
3. O carro libera o desembarque ao esperar barreira barr. Adquire lk e dorme \(cv\_car\) até ficar vazio
4. Repete até limite\_pessoas vezes

### Passageiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_passageiro | Número único que identifica um passageiro | inteiro |
| carro | Referência ao único carro da montanha-russa | [Carro](#Carro) |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| cv\_fila | Utilizado para garantir exclusão mútua \(vide documentação do python\) com outros passageiros tentando entrar na fila. Utilizado para que a thread do passageiro durma enquanto não é o primeiro da fila \(acordado pelo carro\) | [Condition](https://docs.python.org/3/library/threading.html#condition-objects) |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | Simula o comportamento de um passageiro |
| entrar\_fila | Chama o método entrar\_fila do carro |
| passear | Simula o passageiro indo em outros brinquedos no barque antes de voltar à montanha-russa |
| board | Chama o método board do carro |
| unboard | Chama o método unboard do carro |

#### Condições e fluxo

1. O passageiro entra na fila e notifica o carro
2. O passageiro espera sua vez
3. O passageiro é acordado e entra no carro, notificando-o
4. Espera o passeio terminar \(espera barreira\)
5. O passageiro sai do carro \(adquire lk\) e notifica o carro caso for o último a sair
6. O passageiro vai passear
7. Repete



