# Abordagem 2

## Descrição

bla

### Condições e fluxo

Considere o caso em que o carro possui 6 vagas mas há 12 pessoas no parque:

#### Carro

1. O carro espera o evento vazio para liberar o embarque.
2. O carro espera o evento cheio para terminar o embarque e iniciar o passeio.
3. Depois do passeio, é iniciado o desembarque.

#### Fila do carro

1. A fila do carro espera o embarque ser liberado para liberar o passagei o atual.
2. A fila espera o passageiro atual embarcar no carro para chamar o próximo.

#### Passageiros

1. Os passageiros entram na fila e esperam a sua vez.
2. Na sua vez, tentam  alocar um assento do semáforo. Com isso fazendo o controle de limite de pessoas no carro.
3. Depois de alocar o assento eles entram de fato carro.
4. Após embarcarem, eles esperam o desembarque do carro. 
5. Ao desembarcarem, liberam o assento adquirido e vão passear.

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

### Passageiro

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



