from datetime import datetime
from . import db
import pytz

# Definição de modelos de banco de dados:
# Classe User: Representa um usuário do sistema.
# Classe Account: Representa uma conta bancária.
# Classe TransactionType: Representa um tipo de transação financeira (entrada ou saída).
# Classe Revenue: Representa uma entrada de dinheiro (receita).
# Classe Expense: Representa uma saída de dinheiro (despesa).
# Classe SavingGoal: Representa uma meta de poupança financeira.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
    accounts = db.relationship('Account', backref='user', lazy=True)
    savings_goals = db.relationship('SavingGoal', backref='user', lazy=True)
    transaction_types = db.relationship('TransactionType', backref='user', lazy=True)

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_balance = db.Column(db.Float, nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
    revenues = db.relationship('Revenue', backref='account', lazy=True)
    expenses = db.relationship('Expense', backref='account', lazy=True)

class TransactionType(db.Model):
    __tablename__ = 'transaction_types'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_name = db.Column(db.String(50), nullable=False)
    transaction_category = db.Column(db.Enum('revenue', 'expense'), nullable=False)
    revenues = db.relationship('Revenue', backref='transaction_type', lazy=True)
    expenses = db.relationship('Expense', backref='transaction_type', lazy=True)

class Revenue(db.Model):
    __tablename__ = 'revenues'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('transaction_types.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    revenue_date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('transaction_types.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

class SavingGoal(db.Model):
    __tablename__ = 'saving_goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False, default=0.00)
    target_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
