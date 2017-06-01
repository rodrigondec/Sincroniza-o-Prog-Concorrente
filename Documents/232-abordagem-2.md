# Abordagem 2

## Descrição

Essa abordagem utiliza [Locks](https://docs.python.org/3/library/threading.html#lock-objects), [Variáveis Condicionais](https://docs.python.org/3/library/threading.html#condition-objects), [Barreiras](https://docs.python.org/3/library/threading.html#barrier-objects) e [Semáforos](https://docs.python.org/3/library/threading.html#semaphore-objects): objetos disponibilizados pela biblioteca threading de python 3. Quanto à estrutura de dados, uma "fila" é utilizada \(na realidade apenas a lista padrão de python é utilizada, mas os métodos chamados simulam o comportamento de uma fila\).

Na simulação, cada passageiro corresponde à uma thread, bem como cada carro. Há uma fila de entrada para evitar starvation das threads de passageiros \(enquanto esperam entrar em um carro\). Os locks estão sendo utilizados para garantir exclusão mútua e consistência, i.e. operações de inserção e remoção nas listas. As variáveis condicionais estão sendo utilizadas para economozar tempo e processamento desnecessário; por exemplo, quando um passageiro tem que esperar ser o primeiro da fila para poder entrar no carro. A barreira é utilizada para liberar a saída dos passageiros dos carros, como se fosse uma variável condicional compartilhada. Por último, os semáforos são usados para garantir a ordem de chegada dos carros, i.e. garantir que os passageiros do Carro 1 saiam antes dos do Carro 2.

Uma diferença relevante em relação ao problema normal é que, agora, há variáveis globais. A variável curr\_car é usada para armazenar o carro no qual os próximos passageiros devem tentar entrar; fila_cv atual simultaneamente como Lock e Condition para administrar operações na fila de espera; e fila armazena os passageiros que estão na fila de espera.

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
| prv\_car | Referência ao carro anterior. Usado para acordar carro anterior, permitindo que novos passageros embarquem nele enquanto o carro atual começa o passeio | #Carro |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| barr | Utilizado para impedir que passageiros "pulem" da montanha-russa. É utilizado para liberar os passageiros para desembarque | [Barrier](https://docs.python.org/3/library/threading.html#barrier-objects) |
| lk | Utilizado para garantia exclusão mútua e garantir consistência ao realizar operações de adição e remoção em passageiros e/ou fila | [Lock](https://docs.python.org/3/library/threading.html#lock-objects) |
| cv\_car | Utilizado para fazer a thread do carro dormir e esperar que uma condição aconteça para que volte a agir \(carro ficar cheio ou vazio\). Evita processamento desnecessário. | [Condition](https://docs.python.org/3/library/threading.html#condition-objects) |
| sem | Utilizado para controlar operação de unboard. Garantindo que um carro não "ultrapasse" o outro e que os passageiros do primeiro carro vão sair antes dos passageiros do segundo. | [Semáforo](https://docs.python.org/3/library/threading.html#semaphore-objects) |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| main | Simula o comportamento de um carro da montanha russa. Executa o ciclo de vida num\_passeio vezes |
| run | Simula o carro andando na montanha-russa. Thread dorme por um tempo |
| load | Operação que permite que passageiros entrem no carro atual. Acorda exatamente limite\_pessoas threads que estejam esperando na fila para que elas entrem no carro. Caso não haja pessoas suficientes na fila, espera alguém entrar nela através do método entrar\_fila. Quando cheio, muda a referência de curr_car para prv\_car para que passageiros possam embarcar no próximo carro vazio |
| unload | Autoriza o desembarque. Thread chama barr.wait\(\), acordando todos os passageiros dentro do carro. Thread dorme enquanto houver passageiros no carro. Thread também adquire próprio semáforo e, depois de vazio, solta o semáforo do carro anterior, garantindo consistência na ordem de chegada |

#### Condições e fluxo

##### Carro

1. O carro libera o embarque, acordando passageiros na fila. Adquire lk. Dorme \(fila\_cv\) caso precise esperar mais passageiros chegarem na fila para ficar cheio. Dorme \(cv\_car\) para esperar que todos os passageiros notificados entrem no carro. Quando estiver cheio, libera o carro prv\_car para realizar embarque.
2. O carro está cheio e anda na montanha russa \(dorme por um determinado tempo\)
3. Adquire o próprio semáforo para esperar os carros à sua frente terminarem desembarque. O carro libera o desembarque ao esperar barreira barr. Adquire lk e dorme \(cv\_car\) até ficar vazio. Quando estiver vazio, libera o semáforo de prv\_car, liberando-o para desembarque
4. Repete até limite\_pessoas vezes

### Passageiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_passageiro | Número único que identifica um passageiro | inteiro |
| carro\_atual | Referência ao carro no qual está embarcado. Se não estiver embarcado, valor é **None** | [Carro](#Carro) |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| cv | Utilizado para que a thread do passageiro durma enquanto estiver na fila e não foi o primeiro \(acordado pelo carro\) | [Condition](https://docs.python.org/3/library/threading.html#condition-objects) |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | Simula o comportamento de um passageiro |
| passear | Simula o passageiro indo em outros brinquedos no barque antes de voltar à montanha-russa |
| board | Operação chamada pelo passageiro. Adiciona passageiro no carro e o notifica \(cv\_car\) para que possa verificar se está cheio. O lock lk deve ter sido adquirido previamente |
| unboard | Operação chamada pelo passageiro. Remove o passageiro do carro e o notifica \(cv\_car\) caso esteja vazio. |
| entrar\_fila | Adquire lock lk para adicionar passageiro na fila de espera. Após adicionar, notifica o carro que pode estar esperando por passageiros para ficar cheio |

#### Condições e fluxo

1. O passageiro entra na fila e notifica o carro
2. O passageiro espera sua vez
3. O passageiro é acordado e entra no carro, notificando-o caso esteja cheio
4. Espera o passeio terminar \(espera barreira\)
5. O passageiro sai do carro \(adquire lk\) e notifica o carro caso for o último a sair
6. O passageiro vai passear
7. Repete



