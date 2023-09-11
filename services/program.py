from sqlalchemy.orm import Session

from ATL.models.program import Program
from ATL.schemas.program import ProgramCreate


def get_program(db: Session, program_id: int):
    return db.query(Program).filter(Program.id == program_id).first()


def get_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Program).offset(skip).limit(limit).all()


def create_program(db: Session, program: ProgramCreate,):
    db_program = Program(id=program.id, title=program.title, licenseKey=program.licenseKey, version=program.version, installLink=program.installLink)
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def update_program(db: Session, program_id: int, program_update: ProgramCreate):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        return None
    for attr, value in program_update.dict().items():
        setattr(db_program, attr, value)
    db.commit()
    return db_program

def delete_program(db: Session, program_id: int):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        return None
    db.delete(db_program)
    db.commit()
    
    return db_program

