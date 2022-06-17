from PIL import Image

#Definindo as extensões de imagem aceitas
ALLOWED_EXTENSIONS = set(['jpg'])

#Método para verificar a se a extensão do arquivo é suportada
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Método para verificar a se o arquivo está corrompido
def valid_file(fileimage):
    try:
        with Image.open(fileimage) as img:
            verify = img.copy()
            verify.verify()
        return True
    except Exception as e:
        print(e)
        return False