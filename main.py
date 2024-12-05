import os
from PIL import Image


def crop_image(image, x, y, width, height):
    """
    Crop the given image to the specified width and height starting from (x, y).
    """
    return image.crop((x, y, x + width, y + height))


def batch_crop_images(input_dir, output_dir, x, y, width, height):
    """
    Crop all images in the input directory with the specified dimensions and save to output directory.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get all image paths
    image_paths = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith((".png", ".jpg", ".jpeg"))
    ]
    if not image_paths:
        print("No images found in the input directory.")
        return

    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                # Ensure crop dimensions do not exceed image size
                img_width, img_height = img.size
                crop_width = min(width, img_width - x)
                crop_height = min(height, img_height - y)
                if (
                    x >= img_width
                    or y >= img_height
                    or crop_width <= 0
                    or crop_height <= 0
                ):
                    print(f"Skipping {image_path} due to invalid crop dimensions.")
                    continue

                # Crop the image
                cropped_img = crop_image(img, x, y, crop_width, crop_height)

                # Save the cropped image to the output directory with the same name
                output_path = os.path.join(output_dir, os.path.basename(image_path))
                cropped_img.save(output_path)
                print(f"Cropped and saved: {output_path}")

        except Exception as e:
            print(f"Error processing {image_path}: {e}")


if __name__ == "__main__":
    input_dir = input("Enter the input directory path: ").strip()
    output_dir = input("Enter the output directory path: ").strip()
    x = int(input("Enter the x-coordinate of the top-left corner (px): "))
    y = int(input("Enter the y-coordinate of the top-left corner (px): "))
    width = int(input("Enter the width of the crop area (px): "))
    height = int(input("Enter the height of the crop area (px): "))

    batch_crop_images(input_dir, output_dir, x, y, width, height)
