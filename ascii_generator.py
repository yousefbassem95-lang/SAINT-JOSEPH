

from PIL import Image
import ascii_magic

try:
    # Open the image
    img = Image.open('WhatsApp Image 2025-12-30 at 7.13.47 AM.jpeg')
    # Convert to RGBA
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # if the pixel is red, make it transparent
        if item[0] > 200 and item[1] < 50 and item[2] < 50:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    # Create an AsciiArt object from the image
    my_art = ascii_magic.AsciiArt.from_pillow_image(img)
    # Display the ASCII art in the terminal with a specified width
    my_art.to_terminal(columns=100)
except FileNotFoundError:
    print("Error: 'WhatsApp Image 2025-12-30 at 7.13.47 AM.jpeg' not found. Make sure the image file is in the correct directory.")
except Exception as e:
    print(f"An error occurred: {e}")

