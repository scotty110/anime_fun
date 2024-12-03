from PIL import Image, ImageDraw, ImageFont

# Load the image
img = Image.open("test.png")  # replace with your own image

# Set the text to be overlaid on the image
text = "Anime!!! This is a longer caption that needs to be wrapped onto multiple lines."

# Define some constants for color and font sizes
BLACK = (0, 0, 0)
FONT_SIZE_BODY = 40

# Get a font object for our text
font_body = ImageFont.truetype("NotoSans.ttf", FONT_SIZE_BODY)

# Create a drawing context
draw = ImageDraw.Draw(img)

# Define some styles for the caption
CAPTION_COLOR = BLACK
CAPTION_PADDING = 5

# Wrap the caption to multiple lines if necessary
lines = []
words = text.split()
current_line = words[0]

for word in words[1:]:
    # Check if adding another word exceeds the image width
    current_text_size = int(draw.textlength(current_line, font=font_body))
    word_size = int(draw.textlength(word, font=font_body))
    if current_text_size + word_size + CAPTION_PADDING > img.width - 2 * CAPTION_PADDING:
        lines.append(current_line)
        current_line = word
    else:
        current_line += ' ' + word

# Add the last line to the list of lines
lines.append(current_line)

# Draw each line of our caption in turn
y = CAPTION_PADDING  # adjust y-coordinate for caption start
for line in lines:
    draw.text((CAPTION_PADDING, y), line, font=font_body, fill=CAPTION_COLOR)
    y += 40 + 5

# Save the new image with caption to disk
img.save("captured_image.jpg")