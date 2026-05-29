# Plugin da SEPE

Plugin com base no pyRevit com ferramentas e automações para a Secretaria de Projetos Estratégicos de Pernambuco.

## Instalação

1. Baixe e execute o arquivo `SEPE-Revit.bat`.
2. Aparecerá uma janela do pyRevit, instale normalmente.
3. Se solicitado, insira a senha (ver com TI).
4. Reinicie o Revit, uma nova aba estará lá.

- Apesar do Plugin da SEPE ser leve, ele precisa baixar o pyRevit, o que pode demorar.
- O arquivo de instalação fará tudo automaticamente. Qualquer dúvida, contatar a Célula BIM.
- Esse processo só acontecerá uma vez, pois as atualizações serão feitas automaticamente.

## Ferramentas implementadas

### Classificar parede por vãos

- Esse botão identifica e escreve no parâmetro `Ambiente` o nível e o ambiente da parede.
- Paredes que não interfaceiam nenhum ambiente permanecerão sem modificações.
- A face de acamento deve estar voltada para o ambiente e não para o núcleo.

## Ferramentas em desenvolvimento

- Classificação de pisos e forros por ambiente, extendendo a função já implementada nas paredes.
- Ajuste de esquadrias e soleiras, adequando-as às dimensões totais da parede (núcleo + revestimentos).
- Identificação automática da necessidade de vergas e contravergas, dependendo do tipo de parede.
- Classificação de paredes por presença de vãos.
- Link para manuais e catálogo de especificações.
