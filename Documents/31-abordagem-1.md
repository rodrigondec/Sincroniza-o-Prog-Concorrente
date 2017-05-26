# Abordagem 1

## Sincronização

A sincronização desse problema foi baseada em variáveis de condição e semáforo.  
Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects) e [BoundedSemaphore](https://docs.python.org/3/library/threading.html#semaphore-objects) objects da biblioteca [threading](https://docs.python.org/3/library/threading.html) do python3.

O Event possiu uma flag `True` ou `False` e um método `wait()` que bloqueia o processo que chamar esse método caso a flag seja `false`.

Enquanto o BondedSemaphore é um Lock com um contador interno com um valor máximo.

Com esses mecanismos podemos sincronizar as threads, verificando condições e bloqueando as threads até que elas sejam satisfeitas.

## Classes

* [Banheiro](#banheiro)
* [Pessoa](#pessoa)

### Banheiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| limite\_pessoas | quantidade de pessoas que cabem no banheiro | inteiro |
| pessoas | quantidade de pessoas no banheiro | inteiro |
| limite\_swap | quantidade de vezes que pessoas do mesmo sexo podem entrar no banheiro | inteiro |
| swap\_atual | quantidade de vezes que pessoas do mesmo sexo entraram no banheiro | inteiro |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| masculino | representa que o banheiro é masculino | Event |
| feminino | representa que o banheiro é feminino | Event |
| vagas | representa as vagas do banheiro | BoundedSemafore |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| swap | método de justiça para starvation de sexo |
| tornar\_masculino | torna o banheiro masculino |
| tornar\_feminino | torna o banheiro feminino |
| tornar\_unissex | torna o banheiro unissex |
| entrar | adiciona uma pessoa no banheiro |
| sair | remove uma pessoa do banheiro |

### Pessoa

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_pessoa | identificador da pessoa | inteiro |
| sexo | sexo da pessoa. 'M' ou 'F' | char |
| thread | representa a vida da pessoa no escritório | Thread |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | representa a vida da pessoa no escritório |
| trabalhar | pessoa trabalha por um tempo |
| esperar\_genero | pessoa verifica o gênero do banheiro |
| entrar | pessoa entra no banheiro |
| sair | pessoa sai do banheiro |

#### Condições

* para uma pessoa querer entrar no banheiro, precisa esperar que ele se torne do seu gênero
* para uma pessoa entrar no banheiro, o banheiro precisa estar `disponível`



