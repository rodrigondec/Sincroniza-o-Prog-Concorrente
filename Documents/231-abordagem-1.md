# Abordagem 1

## Descrição

Essa abordagem utiliza eventos, semáforos e filas. Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects), [BoundedSemaphore](https://docs.python.org/3/library/threading.html#semaphore-objects) e [Queue](https://docs.python.org/3/library/queue.html#queue-objects) objects das bibliotecas [threading](https://docs.python.org/3/library/threading.html) e  [queue](https://docs.python.org/3/library/queue.html) do python3.

## Classes

* [Plataforma](#plataforma)
* [Carro](#carro)
* [Passageiro](#passageiro)

### Plataforma

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| fila\_carros | fila de carros da plataforma | Queue |
| fila\_passageiros | fila de passageiros da plataforma | Queue |
| carro\_atual | carro atual da plataforma | Carro |
| passageiro\_atual | passageiros atual da plataforma | Passageiro |
| thread\_fila\_carros | representa o controlador da fila de carros | Thread |
| thread\_fila\_passageiros | representa o controlador da fila de passageiros | Thread |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| acesso | representa o acesso à plataforma de embarque/desembarque | BoundedSemaphore |
| tem\_carro | representa se tem um carro na plataforma de embarque/desembarque | Event |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| controlador\_fila\_passageiros | controlador da fila de passageiros |
| controlador\_fila\_carros | controlador da fila de carros |
| entrar\_fila\_passageiros | adiciona um passageiro na fila |
| entrar\_fila\_carros | adiciona um carro na fila |

#### Condições e fluxo

##### Fila de carros

1. A fila de carros espera que o passeio do carro atual termine para prosseguir
2. A fila de carros libera a vez do carro atual
3. A fila de carros espera o passeio do carro atual iniciar antes de colocá-lo novamente na fila

##### Fila de passageiros

1. A fila de passageiros espera ter um carro  na plataforma para prosseguir
2. A fila de passageiros espera que o carro atual da plataforma tenha o embarque liberado para prosseguir
3. A fila de passageiros libera a vez do passageiro atual
4. A fila de passageiros espera que o passageiro atual embarque no carro

### Carro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_carro | identificador do carro | inteiro |
| num\_passeios | número de vezes que o carro irá rodar | inteiro |
| limite\_passageiros | quantidade de pessoas que cabem no carro | inteiro |
| passageiros | quantidade atual de pessoas no ca | inteiro |
| thread\_main | representa o controlador do carro | Thread |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| boardable | representa se o embarque do carro está liberado | Event |
| unboardable | representa se o desembarque do carro está liberado | Event |
| assentos | representa os assentos disponíveis no carro | BoundedSemaphore |
| cheio | representa se o carro está cheio | Event |
| vazio | representa se o carro está vazio | Event |
| vez | representa se é a vez do carro | Event |
| passeio\_iniciado | representa se o passeio foi iniciado | Event |
| passeio\_terminado | representa se o passeio terminou | Event |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| main | controlador do carro |
| run | carro passeia no trilho por um tempo |
| load | libera o embarque no carro |
| unload | libera o desembarque no carro |
| board | adiciona um passageiro no carro |
| unboard | remove um passageiro do carro |

#### Condições e fluxo

1. O carro espera sua vez para prosseguir
2. O carro adquire o recurso acesso da plataforma
3. O carro libera o desembarque
4. O carro espera estar vazio para liberar o embarque
5. O carro libera o embarque
6. O carro espera estar cheio para iniciar passeio
7. O carro libera o recurso acesso da plataforma e inicia o passeio

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

#### Condições e fluxo

1. O passageiro entra na fila de passageiros
2. O passageiro espera sua vez
3. O passageiro adquire o recurso assento do carro
4. O passageiro entra no carro
5. O passageiro espera o desembarque do carro ser liberado
6. O passageiro sai do carro
7. O passageiro libera o recurso assento do carro
8. O passageiro vai passear no parque



