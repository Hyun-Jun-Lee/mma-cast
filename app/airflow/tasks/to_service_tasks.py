from datetime import datetime

from app.db.session import get_mongo_db, get_ps_db
from app.db.models import Fighter
from .utils import get_element_safe


def find_all_fighter():
    """
    'fighters' Collection에서 모든 Fighter 정보 수집
    """
    with get_mongo_db() as db:
        collection = db["fighters"]

        documents = collection.find()
        documents_list = list(documents)

    with get_ps_db() as postgres_db:
        for doc in documents_list:
            birth_date = None
            birth_str = get_element_safe(doc, "birth")
            if birth_str:
                try:
                    birth_date = datetime.strptime(birth_str, "%b %d, %Y").date()
                except:
                    birth_date = None

            fighter = Fighter(
                web_fighter_id=get_element_safe(doc, key="web_fighter_id"),
                birth=birth_date,
                name=get_element_safe(doc, key="name"),
                nickname=get_element_safe(doc, key="nickname"),
                height=int(get_element_safe(doc, key="height")),
                weight=int(get_element_safe(doc, key="weight")),
                reach=int(get_element_safe(doc, key="reach")),
                stance=get_element_safe(doc, key="stance"),
                win=int(get_element_safe(doc, key="win")),
                lose=int(get_element_safe(doc, key="lose")),
                draw=int(get_element_safe(doc, key="draw")),
            )

            postgres_db.add(fighter)

        postgres_db.commit()
