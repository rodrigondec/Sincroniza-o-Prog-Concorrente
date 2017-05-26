# Banheiro Unissex

## Descrição do problema

> Um escritório contém um banheiro que pode ser utilizado tanto por homens quanto por mulheres, mas não por ambos ao mesmo tempo. Se um homem estiver no banheiro, outros homens podem entrar, porém eventuais mulheres que desejem utilizar o banheiro devem esperar ele ficar vazio. Se uma mulher estiver no banheiro, outras mulheres podem entrar, porém eventuais homens que desejem utilizar o banheiro devem esperar ele ficar vazio. Cada pessoa \(homem ou mulher\) pode passar um tempo utilizando o banheiro.
>
> Projete e implemente uma solução concorrente para o problema. O programa deve exibir a entrada e saída de uma pessoa \(homem ou mulher\) do banheiro bem como quantas pessoas \(homens ou mulheres\) estão no banheiro no momento. Por ser um espaço de tamanho relativamente diminuto, o banheiro possui uma capacidade limite de pessoas C \(fornecida como entrada via linha de comando ou prefixada como um valor constante\) que podem utiliza-lo ao mesmo tempo e o tempo que cada pessoa passa no banheiro é randômico e diferente a cada execução do programa.

## Análise do problema

Os pontos a serem abordados nesse problema são:

1. Um banheiro ser unissex, feminino ou masculino
2. Limite de pessoas dentro do banheiro
3. Caso o banheiro seja de um gênero X, pessoas do gênero X que cheguem depois dele entram; enquanto pessoas do gênero Y esperam
   1. Caso o banheiro seja masculino, quantos outros homens podem entrar deixando que as mulherem fiquem esperando? \(starvation\)



