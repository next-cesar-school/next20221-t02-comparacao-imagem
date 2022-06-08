import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

#Inicializando o API
app2 = Flask(__name__)


#Definindo uma variável para armazenar o caminho da pasta onde serão armazenados os arquivos upados pelo usuário
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload')

#Rota para fazer o upload de um arquivo
@app2.route('/upload', methods=["POST"])
def upload():
    #Recebe um arquivo image do usuário e armazena na variável file
    file = request.files["image"]
    print(UPLOAD_FOLDER)
    print(secure_filename(file.filename))
    #Criando uma variável que irá armazenar o caminho aonde o arquivo deverá ser armazenado. O Método secure_filename serve para eliminar carcteres especiais do titulo do arquivo
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    #Salvando a variável no caminho definido na linha de cima
    file.save(savePath)
    return "Upload feito com sucesso"


if __name__ == "__main__":
    #app2.run(debug=True)
    app2.run()