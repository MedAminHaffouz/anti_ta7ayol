from PIL import Image
import sys
import pytesseract

class ImageProcessor:
    @staticmethod
    def extract_text(image_path: str) -> str:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang= 'ara+eng+fra')
        return text

if __name__ =='__main__':
    image_path = sys.argv[1]

    text = ImageProcessor.extract_text(image_path)
    print("transcript: {}".format(text))
