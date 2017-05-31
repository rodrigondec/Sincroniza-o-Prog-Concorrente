# Abordagem 2

## Descrição

Essa abordagem utiliza apenas os [Locks](https://docs.python.org/3/library/threading.html#lock-objects) e [Variáveis Condicionais](https://docs.python.org/3/library/threading.html#condition-objects) ofertados pela biblioteca threading de python3.

Quanto à estrutura de dados, apenas uma lista foi utilizada para armazenar as pessoas esperando na fila para entrar no banheiro.

Os locks são usados para garantir exclusão mútua e as variáveis condicionais para evitar processamente inútil, fazendo com que uma thread durma.

Resumindo a lógica: há uma fila única na qual entram homens e mulheres. O banheiro ou está vazio ou comportando pessoas de um dos gêneros. Quando a primeira pessoa na fila é de um gênero diferente, espera-se o banheiro esvaziar para que entre.

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

1. O banheiro começa sem gênero
2. O banheiro só tem uma fila, não qual entrarão pessoas dos dois gêneros
3. Quando o banheiro está vazio \(sem gênero\)
   1. Se a fila estiver vazia, espera alguém chegar
   2. Se tiver alguém na fila, atribua seu gênero ao banheiro
4. Quando o banheiro está cheio espere alguém sair
5. Quando tem gente na fila
   1. Se a primeira pessoa é do mesmo gênero do banheiro, incremente o contador e acorde-a
   2. Senão se o contador **não** atingiu o valor máximo, acorde a próxima pessoa do gênero do banheiro
   3. Senão espera o banheiro esvaziar \(gênero será trocado\)

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

1. Cada pessoa trabalha por um tempo aleatório antes de usar o banheiro
2. Pessoa entra na fila, notifica banheiro \(pode estar dormindo caso a fila esteja vazia\) e espera ser acordada para entrar no banheiro
3. Pessoa entra no banheiro
4. Pessoa usa o banheiro \(thread dorme por tempo aleatório\)
5. Pessoa sai do banheiro e notifica o banheiro \(que pode estar dormindo caso estiver cheio\)



