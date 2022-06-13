from ast import Await, Compare, Return
from cgi import FieldStorage
from importlib.resources import path
from msilib.schema import File
import os, json
from pickle import GET
import re
from select import select
from site import removeduppaths
from tkinter import Image
from unittest.mock import patch
from anyio import open_file, sleep_until
from flask import Flask, render_template, request, Response, stream_with_context
from importlib_metadata import files
from numpy import append
import werkzeug
from werkzeug.utils import secure_filename
from modulo import compare
from fastapi import FastAPI, File, UploadFile
from werkzeug import datastructures
from time import sleep
from PIL import Image
#Inicializando o API

app2 = Flask(__name__)


#Definindo uma variável para armazenar o caminho da pasta onde serão armazenados os arquivos upados pelo usuário
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload')
TEMP_FOLDER = os.path.join(os.getcwd(),'temp')



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
    #Criar id das imagens

    id_arq = []
    dir_list_final = []    
    for i in range(len(dir_list)):
        id_arq.append(i+1)
        dir_list_final.append(f"{id_arq[i]} - {dir_list[i]}")
 #converter para json e gerar lista de imagens e seus ids
    return Response(json.dumps(dir_list_final),  mimetype='application/json') 

#@app2.route('/comparation')
    #comparar e retornar a imagem com menor distancia de hamming
    #código base quase pronto
    #chamar codigo de bianka


@app2.route('/remove', methods=["GET"])
def remove():
    path = UPLOAD_FOLDER
    dir_list = os.listdir(path) 
    file = dir_list[int(input('Digite o ID do arquivo que queira excluir: '))]
    removepath = os.path.join(UPLOAD_FOLDER, file)
    os.remove(removepath)
   

    #caminho do arquivo 
    #mostrar os arquivos
    #selecionar os arquivos a serem removidos(lista da route('/list'))
    #remover arquivos selecionados


@app2.route('/instantcomparator', methods=["POST", "GET"])
def temp_upload():
    file1 = request.files["image1"]
    file2 = request.files["image2"]
    savePath1 = os.path.join(TEMP_FOLDER,secure_filename(file1.filename))
    savePath2 = os.path.join(TEMP_FOLDER,secure_filename(file2.filename))
    file1.save(savePath1)
    file2.save(savePath2)
    image1 = Image.open(savePath1)
    image2 = Image.open(savePath2)    
    if compare.compare_two_images(image1,image2) > 0:
        diference_percentual = f"A distancia de Hamming entre as duas imagens é: {compare.compare_two_images(image1,image2)}.\n Portanto as imagens são diferentes." 
        return  diference_percentual
    else:
        return "As imagens são iguais. "
# falta excluir as 2 fotos
  
 


        

if __name__ == "__main__":
    app2.run(debug=True)
    #app2.run(debug=True)