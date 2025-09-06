class Config:
    # Senha
    SECRET_KEY = '123456'

    # URI do banco de dados, nesse caso um banco de dados SQLite chamado site.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Desativa o rastreamento de modificações do banco de dados, melhorando o desempenho
    SQLALCHEMY_TRACK_MODIFICATIONS = False