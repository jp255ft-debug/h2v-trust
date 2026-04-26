import qrcode
from io import BytesIO
import base64

def generate_qr_code(certificate_id: str, batch_hash: str) -> str:
    """Gera QR code em base64 contendo o ID do certificado e o hash do lote."""
    payload = f"https://h2v-trust.com/verify/{certificate_id}?hash={batch_hash[:16]}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"