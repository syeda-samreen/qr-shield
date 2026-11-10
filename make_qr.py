import qrcode

img = qrcode.make("http://paypal.com.secure-login.example.xyz/verify")
img.save("test_qr.png")
print("Saved test_qr.png")
