# STL
import base64, math
from PIL import Image, ImageDraw


def image_to_base64_string(image_path: str):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def save_image_obj(image, save_path):
    image.save(save_path)

def crop_to_2_1_aspect_ratio(input_path, output_path):
    # Open the image
    img = Image.open(input_path)

    # Calculate the target width for a 2:1 aspect ratio
    target_width = int(img.height * 2)

    # Calculate the cropping box
    left_margin = (img.width - target_width) // 2
    right_margin = img.width - left_margin
    top_margin = 0
    bottom_margin = img.height

    # Crop the image
    cropped_image = img.crop((left_margin, top_margin, right_margin, bottom_margin))

    # Save the result
    cropped_image.save(output_path)

def color_multiply(image1_path, image2_path, output_path):
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    img2 = img2.resize(img1.size)

    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    weight1 = 0.75 
    weight2 = 0.25 

    multiplied_data = [
        tuple(int((p1 * weight1 + p2 * weight2) // (weight1 + weight2)) for p1, p2 in zip(data1, data2))
        for data1, data2 in zip(img1.getdata(), img2.getdata())
    ]

    multiplied_image = Image.new('RGB', img1.size)
    multiplied_image.putdata(multiplied_data)

    multiplied_image.save("images/test.png")

def three_circular_gradient(radius, color1, color2, color3, output_path, size=(512, 5)):
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    
    center_x, center_y = size[0] // 2, size[1] // 2

    for y in range(size[1]):
        for x in range(size[0]):
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            if distance <= radius:
                gradient = distance / radius
                if gradient <= 0.5:
                    r = int(color1[0] * (1 - gradient*2) + color2[0] * (gradient*2))
                    g = int(color1[1] * (1 - gradient*2) + color2[1] * (gradient*2))
                    b = int(color1[2] * (1 - gradient*2) + color2[2] * (gradient*2))
                else:
                    gradient = (gradient - 0.5) * 2
                    r = int(color2[0] * (1 - gradient) + color3[0] * gradient)
                    g = int(color2[1] * (1 - gradient) + color3[1] * gradient)
                    b = int(color2[2] * (1 - gradient) + color3[2] * gradient)
                draw.point((x, y), (r, g, b))

    image.save(output_path)

def create_elliptical_gradient(width, height, color1, color2, color3, output_path):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    center_x, center_y = width // 2, height // 2
    max_distance = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)

    for y in range(height):
        for x in range(width):
            distance_x = abs(x - center_x)
            distance_y = abs(y - center_y)
            distance = math.sqrt((distance_x / (width / 2)) ** 2 + (distance_y / (height / 2)) ** 2)

            if distance <= 1:
                gradient = distance
                r = int(color1[0] * (1 - gradient) + color2[0] * gradient)
                g = int(color1[1] * (1 - gradient) + color2[1] * gradient)
                b = int(color1[2] * (1 - gradient) + color2[2] * gradient)
            else:
                gradient = (distance - 1) / (max_distance - 1)
                r = int(color2[0] * (1 - gradient) + color3[0] * gradient)
                g = int(color2[1] * (1 - gradient) + color3[1] * gradient)
                b = int(color2[2] * (1 - gradient) + color3[2] * gradient)

            draw.point((x, y), (r, g, b))

    image.save(output_path)