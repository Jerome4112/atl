from sqlalchemy.orm import Session
from ATL.models.program import Program
from ATL.schemas.program import ProgramCreate

# Funktion zur Abfrage eines Programms anhand seiner ID
def get_program(db: Session, program_id: int):
    """
    Gibt die Daten eines Programms anhand seiner ID zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param program_id: Die ID des Programms.
    :type program_id: int
    :return: Die Programmdaten.
    :rtype: Program
    """
    return db.query(Program).filter(Program.id == program_id).first()

# Funktion zur Abfrage einer Liste von Programmen mit optionalen Überspringen und Begrenzen
def get_programs(db: Session, skip: int = 0, limit: int = 100):
    """
    Gibt eine Liste von Programmen zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param skip: Die Anzahl der Programme, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Programme, die zurückgegeben werden sollen.
    :type limit: int
    :return: Eine Liste von Programmen.
    :rtype: list[Program]
    """
    return db.query(Program).offset(skip).limit(limit).all()

# Funktion zur Erstellung eines neuen Programms
def create_program(db: Session, program: ProgramCreate):
    """
    Erstellt ein neues Programm.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param program: Die Daten des neuen Programms.
    :type program: ProgramCreate
    :return: Die erstellten Programmdaten.
    :rtype: Program
    """
    db_program = Program(id=program.id, title=program.title, licenseKey=program.licenseKey, version=program.version, installLink=program.installLink)
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

# Funktion zur Aktualisierung eines Programms anhand seiner ID
def update_program(db: Session, program_id: int, program_update: ProgramCreate):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        return None
    for attr, value in program_update.dict().items():
        setattr(db_program, attr, value)
    db.commit()
    return db_program

# Funktion zum Löschen eines Programms anhand seiner ID
def delete_program(db: Session, program_id: int):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        return None
    db.delete(db_program)
    db.commit()
    return db_program
