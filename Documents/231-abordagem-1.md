# Abordagem 1

## Descrição

Essa abordagem utiliza eventos, semáforos e filas. Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects), [BoundedSemaphore](https://docs.python.org/3/library/threading.html#semaphore-objects) e [Queue](https://docs.python.org/3/library/queue.html#queue-objects) objects das bibliotecas [threading](https://docs.python.org/3/library/threading.html) e  [queue](https://docs.python.org/3/library/queue.html) do python3.

Os eventos são utilizados para controlar as fases de embarque e desembarque do veículo e as situações cheio e vazio. O controle do acesso aos assentos do carro é feito por um semáforo e pela fila.

### Condições e fluxo

Considere o caso em que uma plataforma possui 2 carros, cada um possuindo 6 vagas mas há 12 pessoas no parque:

#### Plataforma

##### Fila de carros

1. A fila de carros espera que o passeio do carro atual termine para prosseguir
2. A fila de carros libera a vez do carro atual
3. A fila de carros espera o passeio do carro atual iniciar antes de colocá-lo novamente na fila e liberar o próximo

##### Fila de passageiros

1. A fila de passageiros espera ter um carro  na plataforma para prosseguir
2. A fila de passageiros espera que o carro atual da plataforma tenha o embarque liberado para prosseguir
3. A fila de passageiros libera a vez do passageiro atual
4. A fila de passageiros espera que o passageiro atual embarque no carro para poder liberar o próximo

#### Carro

1. O carro espera sua vez para prosseguir
2. O carro adquire o recurso plataforma
3. O carro libera o desembarque
4. O carro espera estar vazio para liberar o embarque
5. O carro libera o embarque
6. O carro espera estar cheio para iniciar passeio
7. O carro libera o recurso plataforma e inicia o passeio

#### Fila do carro

1. A fila do carro espera o embarque ser liberado para liberar o passagei o atual
2. A fila espera o passageiro atual embarcar no carro para chamar o próximo

#### Passageiro

1. O passageiro entra na fila
2. O passageiro espera sua vez
3. O passageiro adquire o recurso assento
4. O passageiro entra no carro
5. O passageiro espera o desembarque do carro ser liberado
6. O passageiro sai do carro
7. O passageiro libera o recurso assento
8. O passageiro vai passear no parque

## Classes

* [Plataforma](#plataforma)
* [Carro](#carro)
* [Passageiro](#passageiro)

### Plataforma

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |
|  |  |  |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |
|  |  |  |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
|  |  |
|  |  |
|  |  |

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



