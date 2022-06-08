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
    file = request.files["imagem"]
    print(UPLOAD_FOLDER)
    print(secure_filename(file.filename))
    #
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    #
    file.save(savePath)
    return "Upload feito com sucesso"


if __name__ == "__main__":
    #app2.run(debug=True)
    app2.run()