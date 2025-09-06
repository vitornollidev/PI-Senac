# Importa a função create_app e o objeto db do módulo app
from app import create_app, db

# Cria uma instância da aplicação
app = create_app()

# Cria o banco de dados e as tabelas
with app.app_context():
    db.create_all()

# Inicia a aplicação em modo de depuração
if __name__ == '__main__':
    app.run(debug=True)
