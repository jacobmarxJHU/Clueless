from app import db

# Utility function to commit changes to database as they're made
def commit_changes():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def emptyArr():
    return ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

def emptyDict():

    outDict = {
        "row0": emptyArr(),
        "row1": emptyArr(),
        "row2": emptyArr(),
        "row3": emptyArr(),
        "row4": emptyArr(),
        "row5": emptyArr(),
        "row6": emptyArr(),
        "row7": emptyArr(),
        "row8": emptyArr(),
        "row9": emptyArr(),
        "row10": emptyArr(),
        "row11": emptyArr(),
        "row12": emptyArr(),
        "row13": emptyArr(),
        "row14": emptyArr(),
        "row15": emptyArr(),
        "row16": emptyArr(),
        "row17": emptyArr(),
        "row18": emptyArr(),
        "row19": emptyArr()
    }

    return outDict