import pyqrcode
from PIL import Image

link = input('Enter Your Link : ')

qr_code = pyqrcode.create(link)

qr_code.png('QR_Code.png',scale=10)

Image.open('QR_Code.png')

