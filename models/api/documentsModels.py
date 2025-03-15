from pydantic import BaseModel


class DocumentUploadRequest(BaseModel):
    filename: str
    file_data: str
