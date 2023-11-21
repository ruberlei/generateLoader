
# Generate Loader

Gerador de script loader baseado em um csv.   
## Funcionalidades

- Gerar script de criação da tabela baseado em csv;
- Gerar arquivos de configuração do loader;
- Executar criação da tabela no banco de dados;
- Executar importação via sqllodaer;

## Executando generateLoader

Clone o projeto

```bash
  git clone https://github.com/ruberlei/generateLoader
```

Entre no diretório do projeto

```bash
  cd generateLoader
```

Instale os requerimentos.

```bash
  pip install -R requirements.txt
```

Observação: Caso utilize Windows para gerar o script e execute o .sh gerado no Linux é preciso executar o comando abaixo:

```
sed -i -e 's/\r$//' arquivo_gerado.sh
```