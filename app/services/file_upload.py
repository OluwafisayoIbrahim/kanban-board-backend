import os
import uuid
from typing import Optional
from PIL import Image
from io import BytesIO
from app.db.supabase_client import supabase, supabase_admin

class FileUploadService:
    def __init__(self):
        self.bucket_name = "profilepicture"  
        self.max_file_size = 5 * 1024 * 1024
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
   
    def validate_image(self, file_content: bytes, filename: str) -> bool:
        """Validate image file"""
        if len(file_content) > self.max_file_size:
            raise ValueError("File size too large. Maximum 5MB allowed.")
       
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in self.allowed_extensions:
            raise ValueError(f"Invalid file type. Allowed: {', '.join(self.allowed_extensions)}")
   
        try:
            Image.open(BytesIO(file_content))
            return True
        except Exception:
            raise ValueError("Invalid image file")
   
    def resize_image(self, file_content: bytes, max_size: tuple = (400, 400)) -> bytes:
        """Resize image to reduce file size"""
        try:
            image = Image.open(BytesIO(file_content))
           
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
           
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
           
            output = BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
   
    def upload_profile_picture(self, user_id: str, file_content: bytes, filename: str) -> Optional[str]:
        """Upload profile picture to Supabase storage"""
        try:
            self.validate_image(file_content, filename)
           
            resized_content = self.resize_image(file_content)
           
            file_ext = os.path.splitext(filename)[1].lower()
            unique_filename = f"{user_id}_{uuid.uuid4()}{file_ext}"
           
            # Use admin client to bypass RLS policies
            client_to_use = supabase_admin if supabase_admin else supabase
            if not supabase_admin:
                print("⚠️  Warning: Using regular client for upload - may fail due to RLS policies")
           
            response = client_to_use.storage.from_(self.bucket_name).upload(
                path=unique_filename,
                file=resized_content,
                file_options={"content-type": f"image/{file_ext[1:]}"}
            )
           
            if response:
                public_url = client_to_use.storage.from_(self.bucket_name).get_public_url(unique_filename)
                return public_url
           
            return None
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
   
    def delete_profile_picture(self, file_path: str) -> bool:
        """Delete profile picture from Supabase storage"""
        try:
            filename = file_path.split('/')[-1]
            
            # Use admin client to bypass RLS policies
            client_to_use = supabase_admin if supabase_admin else supabase
            if not supabase_admin:
                print("⚠️  Warning: Using regular client for delete - may fail due to RLS policies")
            
            response = client_to_use.storage.from_(self.bucket_name).remove([filename])
            return bool(response)
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False