# app/utils/ppt_convertor.py
import os
import traceback
import aspose.slides as slides  # type: ignore

def convert_pptx_to_images(ppt_path, file_id, upload_folder="uploads"):
    abs_ppt_path = os.path.abspath(ppt_path)
    output_folder = os.path.abspath(os.path.join(upload_folder, file_id, "slide_images"))
    os.makedirs(output_folder, exist_ok=True)
    slide_image_paths = []

    with slides.Presentation(abs_ppt_path) as presentation:
        print(f"Loaded presentation. Total slides: {len(presentation.slides)}")
        for i, slide in enumerate(presentation.slides):
            slide_image_path = os.path.join(output_folder, f"slide_{i + 1}.png")
            try:
                if hasattr(slide, "get_image"):
                    image = slide.get_image(2.0, 2.0)
                else:
                    image = slide.get_thumbnail(2.0, 2.0)
                image.save(slide_image_path, slides.ImageFormat.PNG)
            except Exception as slide_err:
                print(f"ERROR rendering slide {i + 1}: {slide_err}")
                traceback.print_exc()
                raise  
            slide_image_paths.append(slide_image_path)
            print(f"Saved slide {i + 1} to {slide_image_path}")

    return slide_image_paths