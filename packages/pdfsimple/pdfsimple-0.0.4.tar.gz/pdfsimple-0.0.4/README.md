pdfsimple
=====================

#### Esse pacote usado para fazer adição de texto e imagens de forma simplificada a um arquivo pdf criado no momento da execução

#### Imagem adicionada a um exemplo:

![image adicionada a um exemplo](IMG/grafico.png)

#### Imagem depois de adicionada a um pdf:

![image adicionada a um exemplo](IMG/imgnopdf.jpg)

## instalação:

`pip install pdfsimple`

## USO:
```
from pdfsimple import PDF

pdf = PDF("local_do_arquivo/nome_do_arquivo.formato")
c.addText('texto', 'center', 'titulo')
c.addimage('imagem', 'center')
pdf.salvar()
```