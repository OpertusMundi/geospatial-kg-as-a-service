from typing import List, Optional

from pydantic import BaseModel


class ConversionDescription(BaseModel):
    input_file_paths: List[str]
    conversion_profile_name: str
    file_to_link_with: Optional[str]
    linking_profile_name: Optional[str]
