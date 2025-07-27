from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulasi database
mahasiswa = []

@app.route('/')
def index():
    return render_template('index.html', mahasiswa=mahasiswa)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nama = request.form['nama']
        mahasiswa.append(nama)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update(index):
    if request.method == 'POST':
        mahasiswa[index] = request.form['nama']
        return redirect(url_for('index'))
    return render_template('update.html', index=index, nama=mahasiswa[index])

@app.route('/delete/<int:index>')
def delete(index):
    mahasiswa.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
