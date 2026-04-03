from PIL import Image
import imageProcesser
import ocr

image = Image.open("image/exchange.png")
cropped = imageProcesser.crop(image, 53, 25, 140, 26)
cropped.show()
cropped.save("image/crop.png")

result = ocr.ocr_image(cropped)
print(result)
