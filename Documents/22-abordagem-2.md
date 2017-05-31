# Abordagem 2

## Descrição

Essa abordagem utiliza bla bla bla. Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects), [BoundedSemaphore](https://docs.python.org/3/library/threading.html#semaphore-objects) e [Queue](https://docs.python.org/3/library/queue.html#queue-objects) objects das bibliotecas [threading](https://docs.python.org/3/library/threading.html) e  [queue](https://docs.python.org/3/library/queue.html) do python3.

## Classes

* [Carro](#carro)
* [Passageiro](#passageiro)

### Carro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### Condições e fluxo

##### Carro

1. O carro libera o desembarque
2. O carro espera estar vazio pra liberar o embarque
3. O carro libera o embarque
4. O carro espera estar cheio pra iniciar o passeio
5. O carro inicia o passeio

##### Fila de passageiros

1. A fila do carro espera o embarque ser liberado
2. A fila libera a vez do passageiro atual
3. A fila espera o passageiro atual embarcar no carro

### Passageiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
|  |  |
|  |  |
|  |  |
|  |  |

#### Condições e fluxo

1. O passageiro entra na fila
2. O passageiro espera sua vez
3. O passageiro adquire o recurso assento
4. O passageiro entra no carro
5. O passageiro espera o desembarque do carro ser liberado
6. O passageiro sai do carro
7. O passageiro libera o resurso assento
8. O passageiro vai passear no parque



