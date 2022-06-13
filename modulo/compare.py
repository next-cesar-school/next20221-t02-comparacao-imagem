import imagehash

def compare_two_images(image1, image2):
     # Hash da primeira Imagem
     hash_img1 = imagehash.phash(image1)

     # Hash da segunda Imagem
     hash_img2 = imagehash.phash(image2)

     # Comparação de hash
     Hamming_distance = hash_img1 - hash_img2 
     print(Hamming_distance)
     return Hamming_distance