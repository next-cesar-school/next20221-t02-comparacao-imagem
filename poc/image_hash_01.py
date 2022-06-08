from PIL import Image
import imagehash


# Hash da primeira Imagem
hashcogu1 = imagehash.phash(Image.open('cogu1.jpg'))
print('Cogumelo 1: ' + str(hashcogu1))

# Hash da segunda Imagem
hashcogu2 = imagehash.phash(Image.open('cogu8.jpg'))
print('Cogumelo 2: ' + str(hashcogu2))


# Comparação de hash
if(hashcogu1 == hashcogu2):
    print("As imagens são iguais!")
else:
    print(f'As imagens são diferentes.\nDistância de Hamming: {(hashcogu1 - hashcogu2)}')
