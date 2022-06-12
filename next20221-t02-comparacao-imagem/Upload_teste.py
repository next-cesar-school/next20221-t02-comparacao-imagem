from ast import Compare, Return
from importlib.resources import path
from msilib.schema import File
import os, json
from pickle import GET
from unittest.mock import patch
from flask import Flask, render_template, request, Response
from importlib_metadata import files
from werkzeug.utils import secure_filename
from modulo import compare

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

@app2.route('/list', methods=["GET"])
def list():
    
    #determinar o caminho
    path = UPLOAD_FOLDER
    dir_list = os.listdir(path)
    print("As imagens são", path, " :")
    print(dir_list)
    #converter para json
    return Response(json.dumps(dir_list),  mimetype='application/json') 

#@app2.route('/comparation')
    #comparar e retornar a imagem com menor distancia de hamming
    #código base quase pronto
    #chamar codigo de bianka


#@app2.route('/remove', methods[os.remove])
    #def remove():
    #path= UPLOAD_FOLDER
    #remove.files=os.remove(path)
    #file= remove.files["image"]

    #caminho do arquivo 
    #mostrar os arquivos
    #selecionar os arquivos a serem removidos(lista da route('/list'))
    #remover arquivos selecionados


@app2.route('/instantcomparator', methods=["POST"])
def instantcomparator():
    file1= request.files["image1"]
    file2=request.files["image2"]
    #como converter de requestfile para osfile
    compare.compare_two_images(file1,file2)
    
           
       
 
 


        

if __name__ == "__main__":
    app2.run(debug=True)
    #app2.run(debug=True)