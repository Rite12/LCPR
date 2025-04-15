# -*- coding: utf-8 -*-
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def pre_process_image(plate):
    gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)  
    
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)
    
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    dilated = cv2.dilate(opening, kernel, iterations=1)
    
    return dilated

def enhance_plate_detection(image):
    height, width = image.shape[:2]
    if width > 1000:
        new_width = 1000
        new_height = int(height * (new_width / width))
        image = cv2.resize(image, (new_width, new_height))
    
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    return enhanced_image

def ocr(plate):
    enhanced_plate = enhance_plate_detection(plate)
    
    processed_plate = pre_process_image(enhanced_plate)
    
    cv2.imwrite("processed_plate.jpg", processed_plate)
    
    config_options = "--psm 7 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text1 = pytesseract.image_to_string(processed_plate, config=config_options, lang="eng")
    
    config_options = "--psm 8 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text2 = pytesseract.image_to_string(processed_plate, config=config_options, lang="eng")
    
    text = text1 if len(text1) > len(text2) else text2
    
    text = ''.join(filter(str.isalnum, text))
    
    return text

def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False

if __name__ == "__main__":
    image_path = "D:/LCPR_FAIZ/LCPR/TestImages/car2.jpg"
    image = cv2.imread(image_path)
    
    if image is not None:
        cv2.imshow("Original Image", image)
        
        enhanced = enhance_plate_detection(image)
        processed = pre_process_image(enhanced)
        
        cv2.imshow("Enhanced Image", enhanced)
        cv2.imshow("Processed Image", processed)
        
        plate_text = ocr(image)
        print(f"Hasil OCR: {plate_text}")
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Gagal membaca gambar. Pastikan path benar.")