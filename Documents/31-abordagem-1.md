# Abordagem 1

## Descrição

Essa abordagem utiliza eventos, semáforos e filas. Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects), [BoundedSemaphore](https://docs.python.org/3/library/threading.html#semaphore-objects) e [Queue](https://docs.python.org/3/library/queue.html#queue-objects) objects das bibliotecas [threading](https://docs.python.org/3/library/threading.html) e  [queue](https://docs.python.org/3/library/queue.html) do python3.

## Classes

* [Banheiro](#banheiro)
* [Pessoa](#pessoa)

### Banheiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_banheiro | identificador do banheiro | inteiro |
| limite\_pessoas | quantidade de pessoas que cabem no banheiro | inteiro |
| pessoas | quantidade de pessoas no banheiro | inteiro |
| pessoa\_atual | pessoa atual da fila do banheiro | Pessoa |
| fila | fila atual do banheiro | Queue |
| fila\_masculina | fila de homens para entrar no banheiro | Queue |
| fila\_feminina | fila de mulheres para entrar no banheiro | Queue |
| thread\_fila | representa o controlador da fila do banheiro | Thread |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| masculino | representa se o banheiro é masculino | Event |
| feminino | representa se o banheiro é feminino | Event |
| disponível | representa se o banheiro está disponpivel | Event |
| vazio | representa se o banheiro está vazio | Event |
| vagas | representa as vagas do banheiro | BoundedSemafore |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| trocar gênero | método de justiça para starvation de sexo |
| tornar\_masculino | torna o banheiro masculino |
| tornar\_feminino | torna o banheiro feminino |
| controlar\_fila | método controlador da fila do banheiro |
| entrar\_fila | adiciona uma pessoa na fila do banheiro |
| entrar | adiciona uma pessoa no banheiro |
| sair | remove uma pessoa do banheiro |

#### Condições e fluxo

##### Banheiro

* O banheiro começa com o gênero masculino
* É chamado o método de justiça de gênero nas seguintes condições:
  * Quando uma fila está maior 1.5\*limite\_pessoas do que a outra
  * Uma das filas está vazia enquanto a outra não

##### Fila do banheiro

* A fila atual do banheiro é de acordo com o gênero atual do banheiro. Com isso fazendo o controle de acesso de gênero



1. A fila atual do banheiro espera ele estar disponível
2. A fila atual do banheiro libera a vez da pessoa atual
3. A fila atual do banheiro espera a pessoa atual entrar no banheiro

### Pessoa

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_pessoa | identificador da pessoa | inteiro |
| sexo | sexo da pessoa. 'M' ou 'F' | char |
| thread | representa a vida da pessoa no escritório | Thread |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| vez | representa se é a vez da pessoa na fila | Event |
| entrou | representa se a pessoa entrou no banheiro | Event |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | representa a vida da pessoa no escritório |
| trabalhar | pessoa trabalha por um tempo |
| entrar | pessoa entra no banheiro |
| sair | pessoa sai do banheiro |

#### Condições e fluxo

1. A pessoa entra na fila
2. A pessoa espera sua vez
3. A pessoa adquire o recurso vaga do banheiro
4. Na sua vez, tentam  alocar uma vaga do semáforo. Com isso fazendo o controle de limite de pessoas no banheiro
5. Depois de alocar a vaga eles entram de fato no banheiro
6. Ao saírem  do banheiro, liberam a vaga e vão trabalhar



