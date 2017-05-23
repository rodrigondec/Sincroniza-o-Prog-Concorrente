# Sincronização

A sincronização desse problema foi baseada em variáveis de condição.  
Mais especificamente utilizando [Event](https://docs.python.org/3/library/threading.html#event-objects) objects da biblioteca [threading](https://docs.python.org/3/library/threading.html) do python3.

Esse objeto possiu uma flag `True` ou `False` e um método `wait()` que bloqueia o processo que chamar esse método caso a flag seja `false`.

Dessa forma podemos sincronizar as threads, verificando se a condição foi satisfeita ou esperar até que ela seja satisfeita.

# Classes

* [Banheiro](#banheiro)
* [Pessoa](#pessoa)

## Banheiro

### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| limite\_pessoas | quantidade de pessoas que cabem no banheiro | inteiro |
| limite\_swap | quantidade de vezes que pessoas do mesmo sexo podem entrar no banheiro | inteiro |
| swap\_atual | quantidade de vezes que pessoas do mesmo sexo entraram no banheiro | inteiro |
| pessoas | pessoas no banheiro | list \[\] |

### Atributos condicionais

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| masculino | representa que o banheiro é masculino | Event |
| feminino | representa que o banheiro é feminino | Event |
| disponível | representa que o banheiro não está cheio | Event |

### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| swap | método para justiça de starvation de sexo |
| entrar | adiciona uma pessoa no banheiro |
| sair | remove uma pessoa do banheiro |

## Pessoa

### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_pessoa | identificador da pessoa | inteiro |
| sexo | sexo da pessoa. 'M' ou 'F' | char |
| thread | representa a vida da pessoa no escritório | Thread |

### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | representa a vida da pessoa no escritório |
| trabalhar | pessoa trabalha por um tempo |
| entrar | pessoa entra no banheiro |
| sair | pessoa sai do banheiro |

### Condições

* para uma pessoa entrar no banheiro, o banheiro precisa estar `disponível`
* para uma pessoa masculina entrar no banheiro, o banheiro precisa ser masculino
* para uma pessoa feminina entrar no banheiro, o banheiro precisa ser feminino



