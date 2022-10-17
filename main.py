import cv2

from methods import decrypt, encrypt

with open("text.txt", "r") as file :
    message = file.read()
image_name = 'zebra.png'

source_image = cv2.imread(image_name)
cv2.imshow(image_name, source_image)

information = '123'
brightness = 0.1
countRepeat = 5
key = 1500
blockSize = 3

new_image = encrypt(source_image, key, countRepeat, brightness, information)

decrypt_info = decrypt(new_image, key, countRepeat, brightness, blockSize)

print(decrypt_info)

cv2.imshow(image_name + ' new', new_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

