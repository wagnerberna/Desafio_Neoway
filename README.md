# Desafio Técnico Neoway

## 💡 Objetivo:
API para raspagem de dados fictícios de candidatos aprovados no vestibular, realizando o armazenamento, consulta, inserção, atualização e remoção dos mesmos.

## 🛠 Tecnologias:
- [Python](https://www.python.org/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [SQLite](https://www.sqlite.org/)
- [Insomnia](https://insomnia.rest/)
- [Pytest](https://docs.pytest.org)

## 🔨 Configuração:

Através do terminal clone o diretório usando a chave SSH, crie o ambiente virtual e instale as dependências utilizando os seguintes comandos:
```bash
git clone git@github.com:wagnerberna/Desafio_Neoway.git
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## 📌 Inicialização:

#### API de Consulta, Inserção, Atualização e Remoção dos candidatos:
No terminal inicialize a API com o seguinte comando:
```bash
python app.py
```

## 🎲 Raspagem dos Dados:
A coleta pode ser feita de forma parcial ou completa definindo os parâmetros do método. \
Para iniciar raspagem completa execute o comando:
```bash
python -c "import start; start.scraping()"
```
### Parâmetros permitidos:

**start_page:** número inteiro da página em que será iniciada a coleta. \
**stop_page:** número inteiro da página final da coleta. \
**sleep_time_page:** tempo de espera em segundos entre a coleta de cada página, para evitar que o servidor identifique as requisições como um ataque DDoS, e faça o bloqueio do IP. \
-Nenhum parâmetro é obrigatório, por padrão vai da primeira à última página sem tempo de espera entre requisições de páginas.
Comando demonstrando a ordem dos parâmetros:
```bash
python -c "import start; start.scraping(start_page, stop_page, sleep_time_page)"
```
Exemplo de coleta da página 1000 até 2000 com 5 segundos de intervalo entre páginas:
```bash
python -c "import start; start.scraping(1000, 2000, 5)"
```
## 🔎 Métodos e Rotas de Requisições:
A URL de base para acesso das rotas é:
**http://localhost:5000**

```python
| Metodo | Rota            | Descricao             |
|--------|-----------------|-----------------------|
| Get    | /candidates     | Buscar todos          |
| Get    | /candidate/{ID} | Buscar por ID         |
| Post   | /register       | Adicionar             |
| Put    | /candidate/{ID} | Atuaizar dados por ID |
| Delete | /candidate/{ID} | Deletar por ID        |
```

## 🔒  Testes
Os testes estão localizados no diretório: /tests
Para rodar os testes é necessário executar o comando:
```bash
pytest
```
