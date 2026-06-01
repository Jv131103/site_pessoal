from flask import Flask, render_template, send_from_directory, flash, redirect, url_for
from flask_mail import Mail, Message
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm

from dotenv import load_dotenv
import os

from utils.secret import gerar_chave_secreta

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', gerar_chave_secreta())

# Inicializa o objeto Flask-Mail
mail = Mail(app)


class ContatoForm(FlaskForm):
    nome = StringField('Seu Nome', validators=[DataRequired()])
    email = EmailField('Seu E-mail', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])


@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/sobre')
@app.route("/eu")
@app.route("/mim")
def sobre():
    return render_template('sobre.html')


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        mensagem = form.mensagem.data

        # Enviar o e-mail
        msg = Message(
            subject="Mensagem de Contato",
            recipients=[os.getenv('MAIL_USERNAME')],
            body=f"Nome: {nome}\nE-mail: {email}\nMensagem: {mensagem}",
            reply_to=email
        )
        try:
            # Enviar a mensagem
            mail.send(msg)
            flash('Mensagem enviada com sucesso!', 'success')
            return redirect(url_for('contato'))  # Redireciona para o GET da mesma página, limpando os dados do formulário
        except Exception as e:
            flash(f'Erro ao enviar mensagem: {e}', 'danger')
            return redirect(url_for('contato'))  # Redireciona para o GET da mesma página, limpando os dados do formulário

    return render_template('contato.html', form=form)


@app.route('/curriculo')
def curriculo():
    return render_template('curriculo.html')


# Rota para baixar o PDF
@app.route('/download')
def download():
    return send_from_directory(directory='static/docs', path='João Vitor Justino.pdf', as_attachment=True)


@app.route("/algoritmos")
@app.route("/meus_projetos")
def algoritmos():
    return render_template('algoritmos.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404  # Retorna uma página de erro personalizada


# Manipulador de erro 500 (Erro interno do servidor)
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500  # Retorna uma página de erro personalizada


# Rota para testar os erros
@app.route("/error")
def error():
    raise Exception("Erro de teste")


if __name__ == '__main__':
    from waitress import serve

    # http://localhost:5000/
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
