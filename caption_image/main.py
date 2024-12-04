from PIL import Image, ImageDraw, ImageFont
import io

# Twirp Stuff
import asyncio
import logging

from twirp.context import Context
from twirp.asgi import TwirpASGIApp

import llm_pb2
import llm_twirp


def caption_image(image_bytes, text, font_path="NotoSans.ttf"):
    # Load the image from bytes
    img = Image.open(io.BytesIO(image_bytes))
    original_width, original_height = img.size
    
    # Define some constants for color and font sizes
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)  # White color for the new space
    FONT_SIZE_BODY = 40
    
    # Get a font object for our text
    try:
        font_body = ImageFont.truetype(font_path, FONT_SIZE_BODY)
    except IOError:
        print(f"Error: Font file '{font_path}' not found. Using default font.")
        font_body = ImageFont.load_default()
    
    # Create a drawing context for calculating text size
    draw = ImageDraw.Draw(img)
    
    # Define some styles for the caption
    CAPTION_COLOR = BLACK
    CAPTION_PADDING = 5
    LINE_SPACING = 10
    
    # Wrap the caption to multiple lines if necessary
    lines = []
    words = text.split()
    current_line = words[0]
    for word in words[1:]:
        # Check if adding another word exceeds the image width
        current_text_size = draw.textsize(current_line, font=font_body)[0]
        next_word_size = draw.textsize(word, font=font_body)[0]
        
        if current_text_size + next_word_size + CAPTION_PADDING * 2 > original_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line += ' ' + word
    
    # Add the last line to the list of lines
    lines.append(current_line)
    
    # Calculate the total height needed for the text
    text_height = (len(lines) - 1) * (FONT_SIZE_BODY + LINE_SPACING) + FONT_SIZE_BODY + CAPTION_PADDING * 2
    
    # Create a new image with added white space at the bottom
    new_image_height = original_height + text_height
    new_img = Image.new("RGB", (original_width, new_image_height), WHITE)
    new_img.paste(img, (0, 0))
    
    # Create a drawing context for the new image
    draw = ImageDraw.Draw(new_img)
    
    # Draw each line of our caption in turn
    y = original_height + CAPTION_PADDING
    for line in lines:
        draw.text((CAPTION_PADDING, y), line, font=font_body, fill=CAPTION_COLOR)
        y += FONT_SIZE_BODY + LINE_SPACING
    
    # Return the new image as bytes
    with io.BytesIO() as output:
        new_img.save(output, format='PNG')
        return output.getvalue()


# Twirp
class FrierenCaption(object):
    def __init__(self):
        return 

    def CaptionImage(self, context, req) -> llm_pb2.AImage:
        c_img = caption_image(req.Image, req.Text)

        r_obj = llm_pb2.AImage()
        r_obj.Text = c_img 
        return r_obj


# Start Server
logging.basicConfig()
service = llm_twirp.ImageCaptionServiceServer(service=FrierenCaption())
app = TwirpASGIApp()
app.add_service(service)