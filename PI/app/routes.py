from flask import (Blueprint, request, render_template, redirect,
                   url_for,flash, session, jsonify)
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import pytz

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    from .models import User, TransactionType, Account
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(fullname=fullname, username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()

            transaction_types = [
                TransactionType(type_name='Salário', user_id=new_user.id, transaction_category='revenue'),
                TransactionType(type_name='Alimentação', user_id=new_user.id, transaction_category='expense'),
                TransactionType(type_name='Diversão', user_id=new_user.id, transaction_category='expense'),
                TransactionType(type_name='Transporte', user_id=new_user.id, transaction_category='expense'),
                TransactionType(type_name='Moradia', user_id=new_user.id, transaction_category='expense')
            ]
            db.session.add_all(transaction_types)
            db.session.commit()

            new_account = Account(account_name="Carteira", user_id=new_user.id)
            db.session.add(new_account)
            db.session.commit()
            
            flash('Registrado com sucesso! Faça login.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar usuário. Tente novamente.', 'danger')
            return redirect(url_for('main.register'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    from .models import User
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    from .models import Account, TransactionType, Expense, Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    
    user_id = session['user_id']
    accounts = Account.query.filter_by(user_id=user_id).all()
    expense_types = TransactionType.query.filter_by(user_id=user_id, transaction_category='expense').all()
    revenue_types = TransactionType.query.filter_by(user_id=user_id, transaction_category='revenue').all()

    expenses = Expense.query.join(Account).filter(Account.user_id == user_id).all()
    revenues = Revenue.query.join(Account).filter(Account.user_id == user_id).all()

    total_revenue = db.session.query(db.func.sum(Revenue.amount)).join(Account).filter(Account.user_id == user_id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).join(Account).filter(Account.user_id == user_id).scalar() or 0

    # Preparar dados de despesas por tipo
    expense_data = {expense_type.type_name: 0 for expense_type in expense_types}
    for expense in expenses:
        if expense.transaction_type.type_name in expense_data:
            expense_data[expense.transaction_type.type_name] += expense.amount

    # Preparar os labels e valores para o gráfico
    labels = list(expense_data.keys())
    data = list(expense_data.values())

    # Adicionar valor disponível para gastar, se houver
    if total_revenue > total_expense:
        labels.append('Disponível para Gasto')
        data.append(total_revenue - total_expense)

    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    return render_template('dashboard.html', accounts=accounts, total_revenue=total_revenue,
                           total_expense=total_expense, labels=labels, data=data, expense_types=expense_types,
                           revenue_types=revenue_types, labels_json=labels_json, data_json=data_json, expenses=expenses, revenues=revenues)

@main.route('/add_account', methods=['POST'])
def add_account():
    from .models import Account
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma conta.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    account_name = request.form.get('account_name')

    new_account = Account(account_name=account_name, user_id=user_id)

    db.session.add(new_account)
    db.session.commit()

    flash('Conta cadastrada com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/add_expense', methods=['POST'])
def add_expense():
    from .models import Expense, Revenue, Account
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    amount = request.form.get('amount')
    description = request.form.get('description')
    transaction_type_id = request.form.get('expense.transaction_type_id')
    account_id = request.form.get('account_id')
    expense_date = request.form.get('date')

    amount = float(amount)
    transaction_type_id = int(transaction_type_id)
    account_id = int(account_id)
    expense_date = datetime.strptime(expense_date, '%Y-%m-%d')

    total_revenue = db.session.query(db.func.sum(Revenue.amount)).filter_by(account_id=account_id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).filter_by(account_id=account_id).scalar() or 0
    current_balance = total_revenue - total_expense

    if amount > current_balance:
        flash('Saldo insuficiente na carteira selecionada.', 'danger')
        return redirect(url_for('main.dashboard'))

    new_expense = Expense(
        amount=amount,
        description=description,
        transaction_type_id=transaction_type_id,
        account_id=account_id,
        expense_date=expense_date,
    )

    db.session.add(new_expense)
    db.session.commit()

    flash('Despesa adicionada com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/add_revenue', methods=['POST'])
def add_revenue():
    from .models import Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma receita.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    amount = request.form.get('amount')
    description = request.form.get('description')
    transaction_type_id = request.form.get('revenue.transaction_type_id')
    account_id = request.form.get('account_id')
    revenue_date = request.form.get('date')

    amount = float(amount)
    transaction_type_id = int(transaction_type_id)
    account_id = int(account_id)
    revenue_date = datetime.strptime(revenue_date, '%Y-%m-%d')

    new_revenue = Revenue(
        amount=amount,
        description=description,
        transaction_type_id=transaction_type_id,
        account_id=account_id,
        revenue_date=revenue_date,
    )

    db.session.add(new_revenue)
    db.session.commit()

    flash('Receita adicionada com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/config', methods=['GET', 'POST'])
def config():
    from .models import User, TransactionType, Expense, Revenue, Account
    user_id = session.get('user_id')
    if not user_id:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    expense_types = TransactionType.query.filter_by(user_id=user_id, transaction_category='expense').all()
    revenue_types = TransactionType.query.filter_by(user_id=user_id, transaction_category='revenue').all()
    expenses = Expense.query.join(Account).filter(Account.user_id == user_id).all()
    revenues = Revenue.query.join(Account).filter(Account.user_id == user_id).all()

    if request.method == 'POST':
        user.fullname = request.form.get('fullname')
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password:
            if new_password != confirm_password:
                flash('As senhas não coincidem!', 'danger')
                return redirect(url_for('main.config'))
            else:
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        db.session.commit()
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('main.config'))
    
    return render_template('config.html', user=user, expense_types=expense_types, revenue_types=revenue_types, expenses=expenses, revenues=revenues)

@main.route('/delete_expense_type/<int:id>')
def delete_expense_type(id):
    from .models import TransactionType, Expense
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir um tipo de despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    expense_type = TransactionType.query.get(id)

    if not expense_type or expense_type.user_id != user_id or expense_type.transaction_category != 'expense':
        flash('Você não tem permissão para excluir esse tipo de despesa.', 'danger')
        return redirect(url_for('main.transaction_management'))

    associated_expenses = Expense.query.filter_by(transaction_type_id=id).count()
    if associated_expenses > 0:
        flash('Não é possível excluir este tipo de despesa, pois existem despesas associadas a ele.', 'danger')
        return redirect(url_for('main.transaction_management'))

    db.session.delete(expense_type)
    db.session.commit()
    flash('Tipo de despesa excluído com sucesso!', 'success')
    return redirect(url_for('main.transaction_management'))


@main.route('/delete_revenue_type/<int:id>')
def delete_revenue_type(id):
    from .models import TransactionType, Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir um tipo de receita.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    revenue_type = TransactionType.query.get(id)

    if not revenue_type or revenue_type.user_id != user_id or revenue_type.transaction_category != 'revenue':
        flash('Você não tem permissão para excluir esse tipo de receita.', 'danger')
        return redirect(url_for('main.transaction_management'))

    associated_revenues = Revenue.query.filter_by(transaction_type_id=id).count()
    if associated_revenues > 0:
        flash('Não é possível excluir este tipo de receita, pois existem receitas associadas a ele.', 'danger')
        return redirect(url_for('main.transaction_management'))

    db.session.delete(revenue_type)
    db.session.commit()
    flash('Tipo de receita excluído com sucesso!', 'success')
    return redirect(url_for('main.transaction_management'))


@main.route('/delete_expense/<int:id>')
def delete_expense(id):
    from .models import Expense, Account
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir uma despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    expense = Expense.query.get(id)
    
    account = Account.query.get(expense.account_id)
    if not expense or account.user_id != user_id:
        flash('Você não tem permissão para excluir essa despesa.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(expense)
    db.session.commit()
    flash('Despesa excluída com sucesso!', 'success')
    return redirect(url_for('main.transaction_history'))

@main.route('/delete_revenue/<int:id>')
def delete_revenue(id):
    from .models import Revenue, Account
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir uma receita.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    revenue = Revenue.query.get(id)
    
    account = Account.query.get(revenue.account_id)
    if not revenue or account.user_id != user_id:
        flash('Você não tem permissão para excluir essa receita.', 'danger')
        return redirect(url_for('main.transaction_history'))

    db.session.delete(revenue)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('main.transaction_history'))


@main.route('/change_password', methods=['POST'])
def change_password():
    from .models import User
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    
    if not check_password_hash(user.password, current_password):
        flash('Senha atual incorreta.', 'danger')
        return redirect(url_for('main.config'))
    
    if new_password != confirm_new_password:
        flash('As novas senhas não coincidem.', 'danger')
        return redirect(url_for('main.config'))
    
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('main.config'))

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da conta.', 'success')
    return redirect(url_for('main.login'))

@main.route('/transaction_management', methods=['GET', 'POST'])
def transaction_management():
    from .models import TransactionType
    user_id = session.get('user_id')
    if not user_id:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        if 'expense_type' in request.form:
            expense_type_name = request.form['expense_type']
            if expense_type_name:
                new_expense_type = TransactionType(type_name=expense_type_name, user_id=user_id, transaction_category='expense')
                db.session.add(new_expense_type)
                db.session.commit()
                flash('Novo tipo de despesa adicionado com sucesso.', 'success')
        
        if 'revenue_type' in request.form:
            revenue_type_name = request.form['revenue_type']
            if revenue_type_name:
                new_revenue_type = TransactionType(type_name=revenue_type_name, user_id=user_id, transaction_category='revenue')
                db.session.add(new_revenue_type)
                db.session.commit()
                flash('Novo tipo de receita adicionado com sucesso.', 'success')
    
    expense_types = TransactionType.query.filter_by(user_id=user_id, transaction_category='expense').all()
    revenue_types = TransactionType.query.filter_by(user_id=user_id, transaction_category='revenue').all()
    
    return render_template('transaction_management.html', expense_types=expense_types, revenue_types=revenue_types)

@main.route('/transaction_history')
def transaction_history():
    from .models import Expense, Revenue, TransactionType, Account
    user_id = session.get('user_id')
    if not user_id:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    
    expenses = db.session.query(Expense, TransactionType, Account).join(TransactionType, Expense.transaction_type_id == TransactionType.id).join(Account, Expense.account_id == Account.id).filter(Account.user_id == user_id).all()
    revenues = db.session.query(Revenue, TransactionType, Account).join(TransactionType, Revenue.transaction_type_id == TransactionType.id).join(Account, Revenue.account_id == Account.id).filter(Account.user_id == user_id).all()
    
    expense_data = [{'expense': expense, 'transaction_type': transaction_type, 'account': account} for expense, transaction_type, account in expenses]
    revenue_data = [{'revenue': revenue, 'transaction_type': transaction_type, 'account': account} for revenue, transaction_type, account in revenues]

    return render_template('transaction_history.html', expenses=expense_data, revenues=revenue_data)

@main.route('/add_saving_goal', methods=['POST'])
def add_saving_goal():
    from .models import SavingGoal
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma meta de economia.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    goal_name = request.form.get('goal_name')
    target_amount = request.form.get('target_amount')
    target_date = request.form.get('target_date')

    new_goal = SavingGoal(goal_name=goal_name, user_id=user_id, target_amount=target_amount, target_date=datetime.strptime(target_date, '%Y-%m-%d'))
    db.session.add(new_goal)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/calendar')
def calendar():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    return render_template('calendar.html')

@main.route('/api/events')
def api_events():
    from .models import Expense, Revenue, Account
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])

    expenses = Expense.query.join(Account).filter(Account.user_id == user_id).all()
    revenues = Revenue.query.join(Account).filter(Account.user_id == user_id).all()

    events = []

    for expense in expenses:
        events.append({
            'title': f"Despesa: {expense.amount}",
            'start': expense.expense_date.strftime('%Y-%m-%d'),
            'color': 'red'
        })

    for revenue in revenues:
        events.append({
            'title': f"Receita: {revenue.amount}",
            'start': revenue.revenue_date.strftime('%Y-%m-%d'),
            'color': 'green'
        })

    return jsonify(events)
