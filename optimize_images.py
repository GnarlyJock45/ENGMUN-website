from PIL import Image
import os

def optimize_image(input_path, output_prefix, sizes, is_logo=False):
    """
    Optimize an image for different sizes and convert to WebP
    """
    try:
        with Image.open(input_path) as img:
            # Convert RGBA images to RGB if needed
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, 'white')
                if is_logo:
                    background = Image.new('RGBA', img.size, (255, 255, 255, 0))
                background.paste(img, mask=img.split()[-1])
                img = background

            for size in sizes:
                # Calculate height to maintain aspect ratio
                width = size[0]
                height = size[1]

                # Resize image
                resized_img = img.copy()
                resized_img.thumbnail((width, height), Image.Resampling.LANCZOS)

                # Prepare output path
                output_path = f"{output_prefix}_{width}x{height}.webp"


                # Higher quality settings for logos
                if is_logo:
                    resized_img.save(output_path, 'WEBP', quality=100, method=6, lossless=True)
                else:
                    resized_img.save(output_path, 'WEBP', quality=85, method=6)

                # Save as WebP
                # resized_img.save(
                #     output_path, 
                #     'WEBP', 
                #     quality=85, 
                #     method=6, 
                #     lossless=is_logo
                # )
                
                print(f"Created: {output_path}")

    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_committee_images(static_folder="static"):
    """
    Process all committee images in the static folder
    """
    committees_folder = os.path.join(static_folder, "images", "committees")
    
    # Define sizes
    logo_sizes = [
        (64, 64),    # Small logo for cards
        (128, 128),   # Larger logo if needed
        (256, 256),   # Largest logo if needed
    ]
    
    action_sizes = [
        (640, 360),   # Small screens
        (1280, 720)   # Larger screens
    ]

    # Process each image in the committees folder
    for filename in os.listdir(committees_folder):
        input_path = os.path.join(committees_folder, filename)
        
        # Skip if not an image
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        # Get file name without extension
        name_without_ext = os.path.splitext(filename)[0]
        output_prefix = os.path.join(committees_folder, name_without_ext)
        
        # Process based on image type
        if filename.endswith('_logo.png'):
            optimize_image(input_path, output_prefix, logo_sizes, is_logo=True)
        elif filename.endswith(('_action.jpg', '_action.jpeg')):
            optimize_image(input_path, output_prefix, action_sizes, is_logo=False)

if __name__ == "__main__":
    process_committee_images()