import os, json
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from modulo import compare, validacoes
from PIL import Image




#Inicializando o API
app2 = Flask(__name__)



#Definindo uma variável para armazenar o caminho da pasta onde serão armazenados os arquivos upados pelo usuário, bem como a pasta TEMP
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload')
#Definindo uma variável para armazenar o caminho da pasta TEMP, pasta temporária para armazenação de imagens
TEMP_FOLDER = os.path.join(os.getcwd(),'temp')
#Definindo as extensões de imagem aceitas
ALLOWED_EXTENSIONS = set(['jpg'])



#Rota para fazer o upload de um arquivo
@app2.route('/upload', methods=["POST"])
def upload():
    #Recebe um arquivo image do usuário e armazena na variável file
    file = request.files["image"]
    #Criando uma variável que irá armazenar o caminho aonde o arquivo deverá ser armazenado. O Método secure_filename serve para eliminar carcteres especiais do titulo do arquivo
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    #Salvando a variável no caminho definido na linha de cima
    file.save(savePath)
    #Verificando se o arquivo está corrompido ou se a extensão é aceita
    if validacoes.valid_file(file) and validacoes.allowed_file(file.filename):
        return "Upload feito com sucesso"
    else:
        os.remove(savePath)
        return "Upload não realizado. Rever arquivo utilizado."



# Rota para listar os arquivos do diretório UPLOAD
@app2.route('/list', methods=["GET"])  
def list():
    #determinar o caminho
    path = UPLOAD_FOLDER
    dir_list = os.listdir(path)
    print("As imagens são", path, " :")
    #Criando um dicionário para armazenar a lista dos arquivos, associando um id ao nome do arquivo
    dir_list_final = dict() 
    #Inserindo os valores no dicionário criado acima
    for i in range(len(dir_list)):
        id_arq= (i+1)
        name_arq = dir_list[i]
        dir_list_final[id_arq]= name_arq
    return Response(json.dumps(dir_list_final),  mimetype='application/json')



# Rota remover arquivos do diretório UPLOAD
@app2.route('/remove', methods=["GET"])
def remove():
    path = UPLOAD_FOLDER
    dir_list = os.listdir(path)
    #Criando um dicionário para armazenar a lista dos arquivos, associando um id ao nome do arquivo
    dir_list_final = dict() 
    #Inserindo os valores nas listas criadas acima
    for i in range(len(dir_list)):
        id_arq= (i+1)
        name_arq = dir_list[i]
        dir_list_final[id_arq]= name_arq
    #Recebendo do usúario qual o arquivo será excluido
    file = dir_list_final[int(input('Digite o ID do arquivo que queira excluir: '))]
    print(file)
    #Definindo o caminho do arquivo a ser excluido
    removepath = os.path.join(UPLOAD_FOLDER, file)
    #Excluindo o arquivo
    os.remove(removepath)
    return "Arquivo deletado com sucesso."



@app2.route('/comparationlist', methods=["POST"])
def comparationlist():
    #Recebe um arquivo image do usuário e armazena na variável file
    file = request.files["image"]
    #Criando uma variável que irá armazenar o caminho aonde o arquivo deverá ser armazenado.
    savePath = os.path.join(TEMP_FOLDER, secure_filename(file.filename))
    #Salvando a variável no caminho definido na linha de cima
    file.save(savePath)
    #Verificando se o arquivo está corrompido ou se a extensão é aceita
    if validacoes.valid_file(file) and validacoes.allowed_file(file.filename):
        #Abrindo a imagem que será comparada com todas as imagens da pasta UPLOAD
        fiximage = Image.open(savePath)
        #Gerando uma lista com todas as imagens da pasta UPLOAD
        path = UPLOAD_FOLDER
        dir_list = os.listdir(path) 
        #Criando um dicionário para armazenar a lista dos arquivos, associando um id ao nome do arquivo
        dir_list_final = dict() 
        #Inserindo os valores nas listas criadas acima
        for i in range(len(dir_list)):
            id_arq= (i+1)
            name_arq = dir_list[i]
            dir_list_final[name_arq]= id_arq
        #Inicializando uma lista que armazenará os valores da distancia de hamming para cada uma das comparaçoes feitas
        dif_hamming = []
        #Comparando a imagem base com as demais imagens da pasta UPLOAD e preenchendo a lista com o resultado das comparações
        for i in range(len(dir_list)):
            dif_hamming.append(compare.compare_two_images(fiximage,Image.open(os.path.join(UPLOAD_FOLDER, dir_list[i]))))
        #Apagando o arquivo upado
        os.remove(savePath)
        #Obtendo o menor valor da distancia de hamming    
        print(f'Menor distancia: {min(dif_hamming)}')
        #Obtendo o index da menor distancia de hamming na lista anterior
        print(f'Index: {dif_hamming.index(min(dif_hamming))}')
        #A imagem mais próxima será a de menor valor da distancia de hamming
        close_image = dir_list[dif_hamming.index(min(dif_hamming))]  
        return f'{dir_list_final[close_image]} - {close_image}'      
    else:
        os.remove(savePath)
        return "Rever arquivo utilizado."       
        

 

@app2.route('/instantcomparator', methods=["POST", "GET"])
def temp_upload():
    #Recebendo as duas imagens a serem comparadas
    file1 = request.files["image1"]
    file2 = request.files["image2"]
    #Definindo duas variáveis que armazenarão o caminho onde serão salvas as imagens
    savePath1 = os.path.join(TEMP_FOLDER,'1' + secure_filename(file1.filename))
    savePath2 = os.path.join(TEMP_FOLDER,'2' + secure_filename(file2.filename))
    #Salvando as imagens temporariamente na pasta TEMP
    file1.save(savePath1)
    file2.save(savePath2)
    #Verificando se o arquivo está corrompido ou se a extensão é aceita
    if (validacoes.valid_file(savePath1) and validacoes.allowed_file(file1.filename) and validacoes.valid_file(savePath2) and validacoes.allowed_file(file2.filename)):
        #Abrindo as duas imagens a serem comparadas
        image1 = Image.open(savePath1)
        image2 = Image.open(savePath2)
        #Comparando as imagens
        diference_percentual = compare.compare_two_images(image1,image2)  
        #Excluindo as imagens
        os.remove(savePath1)
        os.remove(savePath2)
        #Avaliando o resultado da comparação das imagens
        return f"{diference_percentual}."     
        
    else:
        os.remove(savePath1)
        os.remove(savePath2)
        return "Rever arquivo utilizado."

        

if __name__ == "__main__":
    app2.run(debug=True)