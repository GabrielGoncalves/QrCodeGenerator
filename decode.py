import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode
from PIL import Image

class QRDecoder:
    @staticmethod
    def load_image(image_path):
        return Image.open(image_path)

    @staticmethod
    def convert_to_grayscale(image):
        return image.convert('L')

    @staticmethod
    def invert_colors(image):
        return Image.eval(image, lambda x: 255 if x < 128 else 0)

    @classmethod
    def decode_qr(cls, image):
        image = cls.load_image(image)
        image = cls.convert_to_grayscale(image)
        image = cls.invert_colors(image)
        return decode(image)

    @classmethod
    def default_decoder(cls, image):
        image = cls.load_image(image)
        return decode(image)

def select_file():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    file_path = filedialog.askopenfilename()
    return file_path

def get_data_qrcode(image_path):
    result = QRDecoder.decode_qr(image_path)
    if result:
        return result[0].data.decode('utf-8') 
    else:
        result_default = QRDecoder.default_decoder(image_path)
        if result_default:
            return result_default[0].data.decode('utf-8')
        else:
            return "Nenhum código QR encontrado ou não foi possível decodificar."

def main():
    file_path = select_file()
    if file_path:
        data_qrcode = get_data_qrcode(file_path)
        print("Dado do QR Code:", data_qrcode)
    else:
        print("Nenhum arquivo selecionado.")

if __name__ == "__main__":
    main()
