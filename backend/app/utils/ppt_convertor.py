# app/utils/ppt_convertor.py
import aspose.slides as slides
import os

def convert_pptx_to_images(ppt_path, file_id):
    output_folder = f"uploads/{file_id}/slide_images"
    os.makedirs(output_folder, exist_ok=True)
    slide_image_paths = []

    with slides.Presentation(ppt_path) as presentation:
        for i, slide in enumerate(presentation.slides):
            image = slide.get_thumbnail(2, 2)
            slide_image_path = os.path.join(output_folder, f"slide_{i + 1}.png")
            image.save(slide_image_path)
            slide_image_paths.append(slide_image_path)

    # Return list of image paths
    return slide_image_paths

