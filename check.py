from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_bytes, force_str, force_text
import secrets
print(secrets.token_hex(14).title())

print(force_text(urlsafe_base64_decode('av9e8f-a47127ae4a97c4e07ca74d77c4c2dfd1')))
