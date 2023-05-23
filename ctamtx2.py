import struct
from PIL import Image
import io

def convert_to_mtxv0(input_image_path, output_mtx_path):
    # Read input image
    image = Image.open(input_image_path)

    # Convert image to RGB mode
    image = image.convert("RGB")

    # Create output file
    with open(output_mtx_path, 'wb') as output_file:
        # Write header (MTXv0 identifier)
        output_file.write(struct.pack('<I', 0x3058544D))

        # Write image data chunks
        image_width, image_height = image.size
        for _ in range(2):
            # Calculate chunk size
            chunk_size = image_width * image_height * 3 + 8

            # Write chunk size
            output_file.write(struct.pack('<I', chunk_size))

            # Save image to temporary JPEG file
            temp_jpeg = io.BytesIO()
            image.save(temp_jpeg, format='JPEG', quality=90)

            # Read JPEG data from temporary file
            temp_jpeg.seek(0)
            jpeg_data = temp_jpeg.read()

            # Write JPEG data
            output_file.write(jpeg_data)

            # Double the size of the image for the second chunk
            image_width *= 2
            image_height *= 2

    print(f"Image converted to MTXv0 format: {output_mtx_path}")

# Example usage
convert_to_mtxv0("input.png", "output.mtx")