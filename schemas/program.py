from pydantic import BaseModel


class ProgramBase(BaseModel):
    id: int
    title: str

class ProgramCreate(ProgramBase):
    licenseKey: str
    version: str
    installLink: str

class Program(ProgramBase):
    licenseKey: str
    version: str
    installLink: str

