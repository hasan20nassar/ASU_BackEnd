import os
import posixpath
from django.conf import settings
from django.core.files.storage import Storage, FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class UniversalMediaStorage(Storage):
    """
    Universal media storage supporting seamless switching via .env:
    - STORAGE_PROVIDER=cloudinary: Cloud storage for Serverless (Vercel) hosting.
    - STORAGE_PROVIDER=local: FileSystemStorage on server disk (Localhost / VPS).

    Supports all file types: images, videos, audio, PDF documents, and archives.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = getattr(settings, "STORAGE_PROVIDER", "local").lower().strip()
        self.local_storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL,
        )

    def is_cloudinary_active(self):
        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "")
        api_key = getattr(settings, "CLOUDINARY_API_KEY", "")
        api_secret = getattr(settings, "CLOUDINARY_API_SECRET", "")
        return (
            self.provider == "cloudinary"
            and bool(cloud_name and api_key and api_secret)
        )

    @staticmethod
    def determine_resource_type(filename):
        """
        Classifies file for Cloudinary:
        - image: JPG, PNG, WEBP, GIF, SVG, etc.
        - video: MP4, WEBM, AVI, MOV, etc.
        - raw: PDF, DOC, DOCX, XLS, XLSX, ZIP, etc. (Preserves file integrity)
        """
        ext = os.path.splitext(filename)[1].lower()
        images = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".ico", ".bmp", ".tiff"}
        videos = {".mp4", ".webm", ".avi", ".mov", ".mkv", ".flv", ".wmv"}

        if ext in images:
            return "image"
        elif ext in videos:
            return "video"
        return "raw"

    def _save(self, name, content):
        name = name.replace("\\", "/")

        # Fallback to local disk storage if Cloudinary is not active
        if not self.is_cloudinary_active():
            return self.local_storage._save(name, content)

        import cloudinary
        import cloudinary.uploader

        # Ensure file pointer is at the beginning
        if hasattr(content, "seek"):
            content.seek(0)

        resource_type = self.determine_resource_type(name)

        dirname, basename = posixpath.split(name)
        folder = posixpath.join("asu_media", dirname).replace("\\", "/").strip("/")
        base_without_ext, ext = posixpath.splitext(basename)

        # For raw resources (PDF, Office documents, zip), include extension in public_id
        # so Cloudinary preserves the filename and download mime-type
        public_id = f"{base_without_ext}{ext}" if resource_type == "raw" else base_without_ext

        upload_options = {
            "folder": folder,
            "public_id": public_id,
            "resource_type": resource_type,
            "overwrite": True,
            "unique_filename": False,
            "use_filename": False,
        }

        upload_result = cloudinary.uploader.upload(content, **upload_options)

        # Return full secure HTTPS URL directly
        secure_url = upload_result.get("secure_url") or upload_result.get("url")
        return secure_url

    def url(self, name):
        if not name:
            return ""

        # If name is already a full URL (e.g. returned by Cloudinary _save)
        if name.startswith("http://") or name.startswith("https://"):
            return name

        # If Cloudinary is active but only a relative path was passed
        if self.is_cloudinary_active():
            import cloudinary.utils
            resource_type = self.determine_resource_type(name)
            url, _ = cloudinary.utils.cloudinary_url(
                name,
                resource_type=resource_type,
                secure=True,
            )
            return url

        # Fallback to local media URL
        return self.local_storage.url(name)

    def exists(self, name):
        if name.startswith("http://") or name.startswith("https://"):
            return False
        if self.is_cloudinary_active():
            return False
        return self.local_storage.exists(name)

    def delete(self, name):
        if not self.is_cloudinary_active():
            return self.local_storage.delete(name)

        import cloudinary.uploader
        try:
            resource_type = self.determine_resource_type(name)
            cloudinary.uploader.destroy(name, resource_type=resource_type)
        except Exception:
            pass

    def size(self, name):
        if not self.is_cloudinary_active():
            return self.local_storage.size(name)
        return 0

    def get_available_name(self, name, max_length=None):
        if not self.is_cloudinary_active():
            return self.local_storage.get_available_name(name, max_length=max_length)
        return name

    def get_valid_name(self, name):
        return name.replace("\\", "/")

    def _open(self, name, mode="rb"):
        if not self.is_cloudinary_active():
            return self.local_storage._open(name, mode=mode)
        raise NotImplementedError("Direct file reading from Cloudinary via _open is not supported.")

