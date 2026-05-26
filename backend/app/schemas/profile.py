from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    degree: str | None = None
    major: str | None = None
    gpa: str | None = None
    ielts: str | None = None
    research_interests: str | None = None
    skills: str | None = None
    publications: str | None = None
    target_countries: str | None = None
    target_fields: str | None = None
    cv_url: str | None = None


class ProfileResponse(ProfileUpdate):
    user_id: int

    model_config = {"from_attributes": True}
