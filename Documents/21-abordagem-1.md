# Abordagem 1

## Sincronização

A sincronização desse problema foi baseada em variáveis de condição.  
Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects) objects da biblioteca [threading](https://docs.python.org/3/library/threading.html) do python3.

Esse objeto possiu uma flag `True` ou `False` e um método `wait()` que bloqueia o processo que chamar esse método caso a flag seja `false`.

Dessa forma podemos sincronizar as threads, verificando se a condição foi satisfeita ou esperar até que ela seja satisfeita.

## Classes

* [Carro](#carro)
* [Passageiro](#passageiro)

### Carro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| limite\_pessoas | quantidade de pessoas que cabem no carro | inteiro |
| num\_passeios | número de vezes que o carro irá rodar | inteiro |
| passageiros | passageiros no carro | list \[\] |
| thread\_main | representa o controlador do carro | Thread |
| thread\_run | representa o passeio do carro nos trilhos | Thread |

#### Atributos condicionais

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| boardable | representa o estágio de embarque do carro | Event |
| unboardable | representa o estágio de desembarque do carro | Event |
| cheio | representa o status lotado do carro | Event |
| vazio | representa o status vazio do carro | Event |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| main | controlador do carro |
| run | carro passeia no trilho por um tempo |
| load | libera o embarque no carro |
| unload | libera o desembarque no carro |
| board | adiciona um passageiro no carro |
| unboard | remove um passageiro do carro |

#### Condições

* Para o embarque do carro ser liberado é necessário que o carro esteja vazio
* Para que o carro esteja na situação `boardable` é necessário que ele não esteja cheio
* Para que o passeio do carro seja iniciado é necessário que o carro esteja cheio
* Para que o desembarque do carro seja liberado é necessário que o passeio tenha terminado
* Para que o carro continue na situação `unboardable` é necessário que ele não esteja vazio

### Passageiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_passageiro | identificador do passageiro | inteiro |
| thread | thread que representa a vida do passageiro no parque de diversões | Thread |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | representa a vida do passageiro no parque de diversões |
| passear | passageiro passeia pelo parque de diversões por um tempo |
| board | passageiro entra no carro da montanha-russa |
| unboard | passageiro sai do carro da montanha-russa |

#### Condições

* Para um passageiro embarcar num carro, o carro precisa estar na situação `boardable`
* Para um passageiro desembarcar de um carro, o caro precisa estar na situação `unboardable`



