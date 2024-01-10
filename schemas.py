from pydantic import BaseModel
import modes.mode as generalMode



class Mode(BaseModel):
    mode : type