# SF Café

Este texto documenta a especificação de um sistema para uma cafeteria, SF Café. O respositório contém recursos para frontend e backend.

**Atenção** Para esse serviço o cliente não necessita de senha para login, apenas o email. Os funcionário devem ser mantidos em
http://localhost:A_PORTA_QUE_VOCE_COLOCOU_EM_ENV/admin 


## Inicializando o backend

Você precisa ter o `docker` e o `docker-compose` instalado em sua máquina. para isso verifique os links de documentação prorietária: [Docker](https://docs.docker.com/engine/install/) e [Docker-compose](https://docs.docker.com/compose/install/), nessa ordem.

Primeiramente leia a [seção de arquivos .env](env) para setar as variáveis de ambiente como senhas de banco de dados. Para instalar todos os pacotes e dependências rode:

```
make build
```

Ou, se estiver usando o windows abra o arquivo `Makefile` e execute linha por linha do bloco `build`. Para saber mais [leia](makefile).

Acesse http://localhost:A_PORTA_QUE_VOCE_COLOCOU_EM_ENV e verá seu serviço rodando.

**Atenção** Se não aparecer o site pode ser porque, a primeira vez que é gerado o banco de dados ele demora para inicializar, dessa forma o django tenta conectar com o banco e não consegue, gerando erro. Verifique o `log` no terminal para ter certeza, mas se for esse o caso, execute:

```bash
make run
```

## Arquivos

<a id="env"></a>
### .env e .env.example

São arquivos que guardam variáveis de ambiente, são geralmente dados que precisam de uma segurança maior e não podem ficar expostos no github, por isso sempre o `.env` fica no `.gitignore` e uma versão sem os dados fica disponível em `.env.example`. Você deve então copiar os dados de `.env.example` para `.env` e colocar os dados. Para isso use o comando abaixo:

```bash
cp .env.example .env
```

<a id="makefile"></a>
### Makefile

É útil para executar blocos de códigos juntos, sem precisar digitar um por um na linhas de comandos, então colocamos grupos de comandos que são utilizados comumente juntos, para usar digite `make` e o nome do bloco, por exemplo:

```bash
make init
```


## Inicializando o frontend

Você precisa ter o `poetry` instalado em sua máquina ou na venv. 

```bash
poetry install
```

```bash
python3 frontend/gui/main_window.py
```

**Atenção** Se o computador não reconhecer o módulo `frontend` rode o comando:

```bash
export PYTHONPATH=/your/path/to/project/root
```

## Especificação dos endpoints API

Acesse http://localhost:A_PORTA_QUE_VOCE_COLOCOU_EM_ENV/api/v1/swagger-ui/


## Stack Utilizada 

Linguagem de programação: Python 3.10
Framework web: Django
Banco de dados: PostgreSQL
Bibliotecas:
• Para interface gráfica Tkinter
• Para geração de relatórios: JasperReports
• Outras ferramentas: Docker, Git