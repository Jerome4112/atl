from fastapi import APIRouter
from ATL.schemas.program import Program, ProgramCreate
#from ATL.schemas.posts import Post, PostCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.program import (
    create_program as create_program_service,
    get_program, get_programs, update_program, delete_program
)
#from ATL.services.posts import create_user_post

router = APIRouter(prefix="/program")

@router.get("/", response_model=list[Program], tags=["Program"])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = get_programs(db, skip=skip, limit=limit)
    return programs


@router.get("/{program_id}", response_model=Program, tags=["Program"])
def read_program(program_id: int, db: Session = Depends(get_db)):
    db_program = get_program(db, program_id=program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

@router.post("/", response_model=Program, tags=["Program"])
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    db_program = get_program(db, program.id)
    if db_program:
        raise HTTPException(status_code=400, detail="Program already registered")
    return create_program_service(db=db, program=program)

@router.put("/{program_id}", response_model=ProgramCreate, tags=["Program"])
def update_program_by_id(program_id: int, program_update: ProgramCreate, db: Session = Depends(get_db)):
    updated_program = update_program(db=db, program_id=program_id, program_update=program_update)
    if not updated_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return updated_program

@router.delete("/{program_id}", response_model=Program, tags=["Program"])
def delete_program_by_id(program_id: int, db: Session = Depends(get_db)):
    deleted_program = delete_program(db=db, program_id=program_id)
    if not deleted_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return deleted_program


