"""Image processing utilities for LibrePOS."""

import uuid
from pathlib import Path

from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def process_user_image(
    file: FileStorage,
    username: str,
    static_folder: str,
    max_size: tuple[int, int] = (400, 400),
    quality: int = 85,
) -> str:
    """Process and save a user profile image.

    Args:
        file: The uploaded file from the form
        username: The username for creating the user directory
        static_folder: The Flask app's static folder path
        max_size: Maximum dimensions (width, height) for the image
        quality: JPEG quality (1-100) for compression

    Returns:
        The relative path to the saved image (for storing in DB)
    """
    # Create a user directory if it doesn't exist
    user_dir = Path(static_folder) / "img" / "users" / username
    user_dir.mkdir(parents=True, exist_ok=True)

    # Get secure filename and add UUID prefix
    original_path = Path(secure_filename(file.filename or "image.png"))
    unique_filename = f"{uuid.uuid4().hex}_{original_path.stem}{original_path.suffix}"

    # Full path for saving
    save_path = user_dir / unique_filename

    # Open and process the image
    with Image.open(file.stream) as original_img:
        # Convert to RGB if necessary (for PNG with transparency)
        if original_img.mode in ("RGBA", "P"):
            processed_img = original_img.convert("RGB")
        else:
            processed_img = original_img

        # Resize maintaining an aspect ratio
        processed_img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image
        processed_img.save(save_path, "JPEG", quality=quality, optimize=True)

    # Return a relative path for database storage
    return f"users/{username}/{unique_filename}"


def delete_user_image(image_path: str, static_folder: str) -> bool:
    """Delete a user's profile image.

    Args:
        image_path: The relative path stored in the database
        static_folder: The Flask app's static folder path

    Returns:
        True if deleted successfully, False otherwise
    """
    if not image_path or image_path.startswith(("default_", "profile_image")):
        return False

    full_path = Path(static_folder) / "img" / image_path
    if full_path.exists():
        full_path.unlink()
        return True
    return False


def process_category_image(
    file: FileStorage,
    static_folder: str,
    max_size: tuple[int, int] = (400, 400),
    quality: int = 85,
) -> str:
    """Process and save a category image.

    Security measures:
    - Uses secure_filename() to sanitize the original filename
    - Generates UUID-prefixed unique filename to prevent overwrites
    - Validates image by opening with PIL (rejects non-images)
    - Converts to RGB and saves as JPEG (strips metadata/EXIF)
    - Resizes to max dimensions to limit storage

    Args:
        file: The uploaded file from the form
        static_folder: The Flask app's static folder path
        max_size: Maximum dimensions (width, height) for the image
        quality: JPEG quality (1-100) for compression

    Returns:
        The relative path to the saved image (for storing in DB)
    """
    # Create categories directory if it doesn't exist
    categories_dir = Path(static_folder) / "img" / "categories"
    categories_dir.mkdir(parents=True, exist_ok=True)

    # Get secure filename and add UUID prefix
    original_path = Path(secure_filename(file.filename or "image.png"))
    unique_filename = f"{uuid.uuid4().hex}_{original_path.stem}.jpg"

    # Full path for saving
    save_path = categories_dir / unique_filename

    # Open and process the image
    with Image.open(file.stream) as original_img:
        # Convert to RGB if necessary (handles PNG transparency, palette mode)
        if original_img.mode in ("RGBA", "P"):
            processed_img = original_img.convert("RGB")
        else:
            processed_img = original_img

        # Resize maintaining aspect ratio
        processed_img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image (strips EXIF metadata)
        processed_img.save(save_path, "JPEG", quality=quality, optimize=True)

    # Return relative path for database storage
    return f"categories/{unique_filename}"


def delete_category_image(image_path: str, static_folder: str) -> bool:
    """Delete a category image.

    Args:
        image_path: The relative path stored in the database
        static_folder: The Flask app's static folder path

    Returns:
        True if deleted successfully, False otherwise
    """
    if not image_path:
        return False

    full_path = Path(static_folder) / "img" / image_path
    if full_path.exists():
        full_path.unlink()
        return True
    return False
