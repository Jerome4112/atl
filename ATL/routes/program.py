from fastapi import APIRouter
from ATL.auth.auth_handler import oauth2_scheme
from ATL.schemas.program import Program, ProgramCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.program import (
    create_program as create_program_service,
    get_program, get_programs, update_program, delete_program
)

# Erstellen eines API-Routers für die Program-Entität
router = APIRouter(prefix="/program")

# Route zum Abrufen einer Liste von Programmen
@router.get("/", response_model=list[Program], tags=["Program"])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt eine Liste von Programmen zurück.

    :param skip: Die Anzahl der Programme, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Programme, die zurückgegeben werden sollen.
    :type limit: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Eine Liste von Programmen.
    :rtype: list[Program]
    """
    programs = get_programs(db, skip=skip, limit=limit)
    return programs

# Route zum Abrufen eines einzelnen Programms anhand seiner ID
@router.get("/{program_id}", response_model=Program, tags=["Program"])
def read_program(program_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt die Daten eines einzelnen Programms anhand seiner ID zurück.

    :param program_id: Die ID des Programms.
    :type program_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die Programmdaten.
    :rtype: Program
    """
    db_program = get_program(db, program_id=program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

# Route zum Erstellen eines neuen Programms
@router.post("/", response_model=Program, tags=["Program"])
def create_program(program: ProgramCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Erstellt ein neues Programm.

    :param program: Die Daten des neuen Programms.
    :type program: ProgramCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die erstellten Programmdaten.
    :rtype: Program
    """
    db_program = get_program(db, program.id)
    if db_program:
        raise HTTPException(status_code=400, detail="Program already registered")
    return create_program_service(db=db, program=program)

# Route zum Aktualisieren eines Programms anhand seiner ID
@router.put("/{program_id}", response_model=ProgramCreate, tags=["Program"])
def update_program_by_id(program_id: int, program_update: ProgramCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Aktualisiert die Daten eines Programms anhand seiner ID.

    :param program_id: Die ID des Programms.
    :type program_id: int
    :param program_update: Die aktualisierten Programmdaten.
    :type program_update: ProgramCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die aktualisierten Programmdaten.
    :rtype: ProgramCreate
    """
    updated_program = update_program(db=db, program_id=program_id, program_update=program_update)
    if not updated_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return updated_program

# Route zum Löschen eines Programms anhand seiner ID
@router.delete("/{program_id}", response_model=Program, tags=["Program"])
def delete_program_by_id(program_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Löscht ein Programm anhand seiner ID.

    :param program_id: Die ID des zu löschenden Programms.
    :type program_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die gelöschten Programmdaten.
    :rtype: Program
    """
    deleted_program = delete_program(db=db, program_id=program_id)
    if not deleted_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return deleted_program
