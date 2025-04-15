import cv2
import matplotlib.pyplot as plt


from PlateExtraction import extraction
from OpticalCharacterRecognition import ocr
from OpticalCharacterRecognition import check_if_string_in_file

image = cv2.imread(r'D:/LCPR_FAIZ/LCPR/TestImages/0020.jpg')
plate = extraction(image)
def show_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show

text = ocr(plate)
text = ''.join(e for e in text if e.isalnum())
print(text, end=" ")
if check_if_string_in_file('D:/LCPR_FAIZ/LCPR/Database/Database.txt', text) and text != "":
    print('Terdaftar')
else:
    print("Tidak Terdaftar")
