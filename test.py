import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

image_path = r"F:/Codes/yolov5/LCPR/TestImages/0013.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Gambar tidak ditemukan:", image_path)
    exit()

# Preprocessing
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)

# Find contours
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

plate_crop = None
for c in contours:
    approx = cv2.approxPolyDP(c, 0.018 * cv2.arcLength(c, True), True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        plate_crop = image[y:y + h, x:x + w]

        # Draw bounding box di gambar asli
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Preprocessing untuk OCR
        gray_plate = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
        gray_plate = cv2.convertScaleAbs(gray_plate, alpha=1.5, beta=10)
        gray_plate = cv2.bilateralFilter(gray_plate, 11, 17, 17)
        plate_thresh = cv2.adaptiveThreshold(gray_plate, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
        _, plate_thresh = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY)

        # OCR config
        config = r'--oem 3 --psm 8 -l plateid -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        try:
            raw_text = pytesseract.image_to_string(plate_thresh, config=config).strip()

            # Tampilkan hasil OCR di atas kotak
            cv2.putText(image, raw_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 0), 2, cv2.LINE_AA)

            print("OCR hasil:", raw_text)
        except pytesseract.TesseractError as e:
            print("Tesseract error:", e)
        break

# Tampilkan hasil akhir
cv2.imshow("Plat dan OCR", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
