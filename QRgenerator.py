import qrcode
from PIL import Image

# taking image which user wants in the QR code center
logo = Image.open('../midi.png')

# taking base width
basewidth = 80

# adjust image size
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

# taking url or text
url = 'Tavo Mama'

# adding URL or text to QRcode
QRcode.add_data(url)

# generating QR code
QRcode.make()

# adding color to QR code
QRimg = QRcode.make_image(fill_color="black", back_color="white").convert('RGB')

# set size of QR code
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)

# save the QR code generated
QRimg.save('../attempt.png')
