from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from app.routers.auth import get_current_user
from app.services.file_upload import FileUploadService
from app.db.crud import update_user_profile_picture, get_user_profile_picture

router = APIRouter()

async def _handle_profile_picture_upload(request: Request, file: UploadFile, current_user: dict):
    """Handles logic for uploading or changing a profile picture"""
    try:
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image")

        file_content = await file.read()
        upload_service = FileUploadService()
        current_pic_url = get_user_profile_picture(current_user["id"])

        public_url = upload_service.upload_profile_picture(
            user_id=current_user["id"],
            file_content=file_content,
            filename=file.filename
        )

        if not public_url:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload image")

        if update_user_profile_picture(current_user["id"], public_url):
            if current_pic_url:
                upload_service.delete_profile_picture(current_pic_url)

            return {
                "message": "Profile picture uploaded successfully",
                "profile_picture_url": public_url,
                "username": current_user["username"],
                "email": current_user["email"],
                "status": "success"
            }
        else:
            upload_service.delete_profile_picture(public_url)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update profile picture")

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/upload-profile-picture")
async def upload_profile_picture(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    return await _handle_profile_picture_upload(request, file, current_user)

@router.put("/profile-picture")
async def change_profile_picture(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    return await _handle_profile_picture_upload(request, file, current_user)

@router.delete("/profile-picture")
async def delete_profile_picture(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    try:
        current_pic_url = get_user_profile_picture(current_user["id"])
        if not current_pic_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No profile picture found")

        upload_service = FileUploadService()
        if upload_service.delete_profile_picture(current_pic_url) and update_user_profile_picture(current_user["id"], None):
            return {
                "message": "Profile picture deleted successfully",
                "profile_picture_url": None,
                "username": current_user["username"],
                "email": current_user["email"],
                "status": "success"
            }

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete profile picture")

    except Exception as e:
        print(f"Delete error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/profile-picture")
async def get_profile_picture(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    profile_picture_url = get_user_profile_picture(current_user["id"])
    return {
        "profile_picture_url": profile_picture_url,
        "username": current_user["username"],
        "email": current_user["email"],
        "status": "success"
    }
