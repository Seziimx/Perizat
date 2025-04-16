import qrcode
import os

def generate_qr_code(data, output_folder):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    file_path = os.path.join(output_folder, f"{data}.png")
    img.save(file_path)
    return file_path
