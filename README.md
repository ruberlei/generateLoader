
# Generate Loader

Gerador de script loader baseado em um csv.   
## Funcionalidades

- Gerar script de criação da tabela baseado em csv;
- Gerar arquivos de configuração do loader;
- Executar criação da tabela no banco de dados;
- Executar importação via sql loader;

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

Exemplo de uso:

```bash
python.exe .\genLoader.py "randomperson 5 teste.csv" "HR/HR@192.168.0.22:1521/pdb"
```

Feito isso, serão gerados 3 arquivos no diretório que executou, um *.ctl (referente ao loader), um *.sql (referente ao create table) e um *.sh (referente ao script que se conecta no banco de dados cria a tabela e faz o load dos dados).

Observação: Caso utilize Windows para gerar o script e execute o .sh gerado no Linux é preciso executar o comando abaixo:

```bash
sed -i -e 's/\r$//' arquivo_gerado.sh
```