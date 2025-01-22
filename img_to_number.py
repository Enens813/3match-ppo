from PIL import Image
import easyocr

reader = easyocr.Reader(['en'])

def image_to_number(image_path):
    """
    Converts an image containing a number to a numeric value using OCR.

    :param image_path: Path to the image file
    :return: Extracted number as an integer or float
    """
    try:
        # Open the image file
        img = Image.open(image_path)

        # Convert image to string using pytesseract
        result = reader.readtext(image_path)

        # Clean up the text and convert it to a number
        # cleaned_text = text.strip()
        #print(result)
        return result
        
    #     if '.' in cleaned_text:
    #         return float(cleaned_text)  # Return as float if it has a decimal
    #     else:
    #         return int(cleaned_text)   # Return as integer
    except Exception as e:
        print(f"Error: {e}")
        return None


# Example usage
image_path = "MPT/lv12.png"  # Replace with your image file

result = image_to_number(image_path)

for r in result:
    print(r)
    
print(len(result))
print(len(result[0]))