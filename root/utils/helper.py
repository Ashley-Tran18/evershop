import os

class HelperConfig():
    def get_absolute_image_path(image_name: str) -> str:
        # Lấy thư mục gốc của dự án (giả sử thư mục gốc nằm trên 2 cấp so với file này)
        # Tùy thuộc vào cấu trúc dự án, logic này có thể thay đổi
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        image_path = os.path.join(project_root, "images", image_name)
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"❌ Image not found: {image_path}")
        
        return image_path