from pydantic import BaseModel


class AgencyGroupResponse(BaseModel):
    agency_group_id: int
    name: str

    class Config:
        from_attributes = True
