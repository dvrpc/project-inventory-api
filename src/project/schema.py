from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from src.geography.schema import GeographyResponse
from src.keyword.schema import KeywordResponse
from src.topic.schema import TopicResponse


class ProjectResponse(BaseModel):
    pub_id: str
    typecode: str
    pub_num: str
    title: Optional[str]
    subtitle: Optional[str]
    abstract: Optional[str]
    createdate: Optional[datetime]
    livedate: Optional[datetime]
    lastupdatedate: Optional[datetime]
    pub_date: Optional[datetime]
    s1: Optional[str]
    s1_id: Optional[str]
    status: Optional[str]
    wpids: Optional[list[str]]

    @field_validator("wpids", mode="before")
    @classmethod
    def extract_wpids(cls, v):
        if not v:
            return v
        return [
            item.WORKPROGRAMID if hasattr(item, "WORKPROGRAMID") else item for item in v
        ]

    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    geographies: list[GeographyResponse] = []
    keywords: list[KeywordResponse] = []
    topics: list[TopicResponse] = []


class ProjectFilters(BaseModel):
    bbox: Optional[str] = None
    geographies: Optional[str] = None
    keywords: Optional[str] = None
    topics: Optional[str] = None
    sort: Optional[str] = None
    project: Optional[str] = None
    status: Optional[str] = None
    zoom: Optional[str] = None
    wpids: Optional[str] = None
    yearFrom: Optional[str] = None
    yearTo: Optional[str] = None

    @classmethod
    def as_query(
        cls,
        bbox: Optional[str] = None,
        geographies: Optional[str] = None,
        keywords: Optional[str] = None,
        topics: Optional[str] = None,
        status: Optional[str] = None,
        sort: Optional[str] = None,
        zoom: Optional[str] = None,
        yearFrom: Optional[str] = None,
        yearTo: Optional[str] = None,
        project: Optional[str] = None,
        wpids: Optional[str] = None,
    ) -> "ProjectFilters":

        return cls(
            bbox=bbox,
            geographies=geographies,
            keywords=keywords,
            topics=topics,
            status=status,
            zoom=zoom,
            sort=sort,
            yearFrom=yearFrom,
            yearTo=yearTo,
            project=project,
            wpids=wpids,
        )
