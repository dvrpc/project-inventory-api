from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from src.geography.schema import GeographyResponse
from src.keyword.schema import KeywordResponse
from src.topic.schema import TopicResponse


class ProjectResponse(BaseModel):
    id: str
    title: Optional[str]
    abstract: Optional[str]
    pub_date: Optional[datetime]
    contact_name: Optional[str]
    contact_email: Optional[str]
    project_link: Optional[str]
    thumbnail_link: Optional[str]
    agency: Optional[str]
    funding_source: Optional[str]
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
    fs: Optional[str] = None
    zoom: Optional[str] = None
    wpids: Optional[str] = None
    yearFrom: Optional[str] = None
    yearTo: Optional[str] = None
    showMore: Optional[bool] = False

    @classmethod
    def as_query(
        cls,
        bbox: Optional[str] = None,
        geographies: Optional[str] = None,
        keywords: Optional[str] = None,
        topics: Optional[str] = None,
        status: Optional[str] = None,
        fs: Optional[str] = None,
        sort: Optional[str] = None,
        zoom: Optional[str] = None,
        yearFrom: Optional[str] = None,
        yearTo: Optional[str] = None,
        project: Optional[str] = None,
        wpids: Optional[str] = None,
        showMore: Optional[bool] = False,
    ) -> "ProjectFilters":

        return cls(
            bbox=bbox,
            geographies=geographies,
            keywords=keywords,
            topics=topics,
            status=status,
            fs=fs,
            zoom=zoom,
            sort=sort,
            yearFrom=yearFrom,
            yearTo=yearTo,
            project=project,
            wpids=wpids,
            showMore=showMore
        )
