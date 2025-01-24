from PIL import Image

# Open the image file
image = Image.open('lv171_crop.png')
resized_image = image.resize((9*4, 11*4))

print(resized_image)

# Save the resized image
resized_image.save('output_image.jpg')