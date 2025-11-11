from pydantic import BaseModel, ConfigDict


class CreateStudent(BaseModel):
    name: str
    last_name: str
    faculty: str
    course: str
    grade: int

    model_config = ConfigDict(from_attributes=True)

class GetStudent(CreateStudent):
    id: int