# Abordagem 1

## Descrição

Essa abordagem utiliza eventos, semáforos e filas. Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects), [BoundedSemaphore](https://docs.python.org/3/library/threading.html#semaphore-objects) e [Queue](https://docs.python.org/3/library/queue.html#queue-objects) objects das bibliotecas [threading](https://docs.python.org/3/library/threading.html) e  [queue](https://docs.python.org/3/library/queue.html) do python3.

Os eventos são utilizados para controlar as fases de embarque e desembarque do veículo e as situações cheio e vazio. O controle do acesso aos assentos do carro é feito por um semáforo e pela fila.

### Condições e fluxo

Considere o caso em que o carro possui 6 vagas mas há 12 pessoas no parque:

#### Carro

1. O carro espera o evento vazio para liberar o embarque
2. O carro espera o evento cheio para terminar o embarque e iniciar o passeio
3. Depois do passeio, é iniciado o desembarque

##### Fila de passageiros

1. A fila do carro espera o embarque ser liberado para liberar o passagei o atual
2. A fila espera o passageiro atual embarcar no carro para chamar o próximo

#### Passageiros

1. Os passageiros entram na fila e esperam a sua vez
2. Na sua vez, tentam  alocar um assento do semáforo. Com isso fazendo o controle de limite de pessoas no carro
3. Depois de alocar o assento eles entram de fato carro
4. Após embarcarem, eles esperam o desembarque do carro
5. Ao desembarcarem, liberam o assento adquirido e vão passear

## Classes

* [Carro](#carro)
* [Passageiro](#passageiro)

### Carro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_carro | identificador do carro | inteiro |
| num\_passeios | número de vezes que o carro irá rodar | inteiro |
| limite\_passageiros | quantidade de pessoas que cabem no carro | inteiro |
| passageiros | quantidade atual de pessoas no ca | inteiro |
| passageiro\_atual | passageiro atual da fila | Passageiro |
| fila | fila de passageiros do carro | Queue |
| thread\_main | representa o controlador do carro | Thread |
| thread\_fila | representa o controlador da fila do carro | Thread |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| boardable | representa se o embarque do carro está liberado | Event |
| unboardable | representa se o desembarque do carro está liberado | Event |
| assentos | representa os assentos disponíveis no carro | BoundedSemaphore |
| cheio | representa se o carro está cheio | Event |
| vazio | representa se o carro está vazio | Event |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| main | controlador do carro |
| controlar\_fila | controlador da fila do carro |
| entrar\_fila | adiciona passageiro na fila do carro |
| run | carro passeia no trilho por um tempo |
| load | libera o embarque no carro |
| unload | libera o desembarque no carro |
| board | adiciona um passageiro no carro |
| unboard | remove um passageiro do carro |

### Passageiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_passageiro | identificador do passageiro | inteiro |
| thread | thread que representa a vida do passageiro no parque de diversões | Thread |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| vez | representa se é a vez do passageiro na fila | Event |
| boarded | representa se o passageiro está dentro do carro | Event |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | representa a vida do passageiro no parque de diversões |
| passear | passageiro passeia pelo parque de diversões por um tempo |
| board | passageiro entra no carro da montanha-russa |
| unboard | passageiro sai do carro da montanha-russa |



