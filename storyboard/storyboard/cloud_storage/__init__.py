"""AutoMusicVideo::storyboard.storage.__init__"""

from .buckets import (
  file_exists,
  move_file,
  list_files,
  generate_files_as_bytes,
  num_files,
  delete_file,
  delete_directory,
  upload_pil_image,
  upload_json,
  download_json,
  download_file,
  upload_file
)

from . import inputs
from . import outputs