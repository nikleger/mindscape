from typing import Optional
import base64
import pyotp
import qrcode
from io import BytesIO

from app.core.config import settings

class MFAManager:
    """Manages Multi-Factor Authentication using TOTP."""
    
    def __init__(self, issuer_name: str = settings.MFA_ISSUER):
        self.issuer_name = issuer_name
    
    def generate_secret(self) -> str:
        """Generate a new TOTP secret."""
        return pyotp.random_base32()
    
    def create_totp(self, secret: str) -> pyotp.TOTP:
        """Create a TOTP object from a secret."""
        return pyotp.TOTP(secret)
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify a TOTP token."""
        totp = self.create_totp(secret)
        return totp.verify(token)
    
    def get_provisioning_uri(self, email: str, secret: str) -> str:
        """Get the provisioning URI for QR code generation."""
        totp = self.create_totp(secret)
        return totp.provisioning_uri(
            name=email,
            issuer_name=self.issuer_name
        )
    
    def generate_qr_code(self, email: str, secret: str) -> str:
        """Generate a QR code as a base64 encoded PNG."""
        uri = self.get_provisioning_uri(email, secret)
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

class MFARequired(Exception):
    """Exception raised when MFA is required but not provided."""
    pass

class InvalidMFAToken(Exception):
    """Exception raised when an invalid MFA token is provided."""
    pass 