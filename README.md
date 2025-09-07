# FinGest - Sistema de Gestão Financeira Pessoal

## 🌐 Acesso à Aplicação

**Site em Produção:** http://34.227.242.86:5000

**Credenciais de Teste:**
- **Usuário:** teste_senac
- **Senha:** 123456

---

## 📋 Sobre o Projeto

O **FinGest** é um sistema web de gestão financeira pessoal desenvolvido em Flask que permite aos usuários controlar suas finanças de forma eficiente. O sistema oferece funcionalidades completas para gerenciamento de contas, transações, metas de poupança e relatórios financeiros.

## 🚀 Funcionalidades Principais

- **Autenticação de Usuários**: Sistema completo de registro e login
- **Gestão de Contas**: Criação e gerenciamento de múltiplas contas bancárias/carteiras
- **Controle de Transações**: Registro de receitas e despesas com categorização
- **Metas de Poupança**: Definição e acompanhamento de objetivos financeiros
- **Dashboard Interativo**: Visualização de resumos financeiros e gráficos
- **Histórico de Transações**: Consulta detalhada de movimentações financeiras
- **Calendário Financeiro**: Visualização de transações por período
- **Configurações Personalizadas**: Customização de tipos de transação

## 👥 Equipe de Desenvolvimento

- **Cleber Alves Guedes**
- **Marcelo Augusto Malange Silva**
- **Paulo Henrique Cardoso dos Santos**
- **Thayanne Cristine da Silva Carrilho**
- **Vitor Hugo Nolli**

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **Banco de Dados**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticação**: Werkzeug (hash de senhas)
- **Fuso Horário**: pytz

## 📦 Dependências

O projeto utiliza as seguintes dependências principais:

```
Flask
Flask-SQLAlchemy
Werkzeug
pytz
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo para Execução

1. **Clone o repositório**
   ```bash
   git clone <https://github.com/vitornollidev/PI-Senac>
   cd "PI"
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # No Windows:
   venv\Scripts\activate
   
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   O banco de dados SQLite será criado automaticamente na primeira execução. O arquivo `site.db` será gerado na pasta `instance/`.

5. **Execute a aplicação**
   ```bash
   python run.py
   ```

6. **Acesse a aplicação**
   Abra seu navegador e acesse: `http://localhost:5000`

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas principais:

- **User**: Dados dos usuários do sistema
- **Account**: Contas bancárias/carteiras dos usuários
- **TransactionType**: Tipos de transação (receita/despesa)
- **Revenue**: Registros de receitas
- **Expense**: Registros de despesas
- **SavingGoal**: Metas de poupança

## 📁 Estrutura do Projeto

```
PI/
├── app/
│   ├── __init__.py          # Configuração da aplicação Flask
│   ├── config.py            # Configurações do sistema
│   ├── models.py            # Modelos do banco de dados
│   ├── routes.py            # Rotas e lógica da aplicação
│   ├── static/              # Arquivos estáticos
│   │   ├── css/            # Estilos CSS
│   │   ├── js/             # Scripts JavaScript
│   │   └── img/            # Imagens
│   └── templates/           # Templates HTML
│       ├── base.html       # Template base
│       ├── login.html      # Página de login
│       ├── register.html   # Página de registro
│       ├── dashboard.html  # Dashboard principal
│       └── ...
├── instance/
│   └── site.db             # Banco de dados SQLite
├── requirements.txt        # Dependências do projeto
└── run.py                 # Arquivo principal de execução
```

## 🚀 Como Usar

1. **Primeiro Acesso**: Registre-se no sistema criando uma conta
2. **Login**: Faça login com suas credenciais
3. **Dashboard**: Visualize o resumo financeiro na página inicial
4. **Contas**: Crie e gerencie suas contas bancárias/carteiras
5. **Transações**: Registre receitas e despesas
6. **Metas**: Defina objetivos de poupança
7. **Relatórios**: Consulte o histórico e relatórios financeiros

## 🔒 Segurança

- Senhas são criptografadas usando hash PBKDF2-SHA256
- Sessões de usuário são gerenciadas de forma segura
- Validação de dados em todas as entradas

## 🐛 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problemas com Banco de Dados
- Delete o arquivo `instance/site.db` e execute novamente
- O banco será recriado automaticamente

### Porta em Uso
- Altere a porta no arquivo `run.py` se necessário
- Ou pare outros serviços que estejam usando a porta 5000

## 📝 Notas de Desenvolvimento

- O sistema está configurado para modo debug (desenvolvimento)
- Para produção, altere `debug=True` para `debug=False` em `run.py`
- Configure uma SECRET_KEY mais segura em `config.py` para produção

## 📞 Suporte

Para dúvidas ou problemas, entre em contato com a equipe de desenvolvimento.

---
