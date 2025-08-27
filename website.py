import os
from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# -------------------------
# CONFIG
# -------------------------
INPUT_FOLDER = "ebook_images"      # folder where images are stored
OUTPUT_PDF = "ebook_editable.pdf"

# If Tesseract is not in PATH, set it manually (Windows users)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------------
# Collect images
# -------------------------
image_files = sorted(
    [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER) if f.lower().endswith((".jpg", ".png"))],
    key=lambda x: int(os.path.splitext(os.path.basename(x))[0])  # sort numerically if files are 1.jpg, 2.jpg...
)

print(f"Found {len(image_files)} images in {INPUT_FOLDER}")

# -------------------------
# Create Editable PDF
# -------------------------
c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
width, height = A4

for img_file in image_files:
    print(f"🔎 OCR on {img_file}...")
    text = pytesseract.image_to_string(Image.open(img_file), lang="eng")

    # Write OCR text into PDF
    c.setFont("Helvetica", 10)
    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 14
        if y < 40:  # move to next page if text overflows
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 40

    c.showPage()  # new page for each image

c.save()
print(f"📕 Editable PDF created: {OUTPUT_PDF}")
