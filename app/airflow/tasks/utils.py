import re
from typing import List

from app.db.session import get_mongo_db
from pymongo import errors
from dags.log import logger


def inch_to_cm(data: str, is_reach=False):
    """
    Inches를 센티미터로 변환합니다.

    :param data: 변환할 데이터 문자열 (예: "6'0"").
    :param is_reach: True일 경우, 리치 데이터로 간주하여 다르게 처리합니다.
    :return: 변환된 센티미터 값.
    """
    if is_reach:
        reach = round((int(re.sub("[^0-9]", "", data)) * 2.54), 1)
        return reach
    H_feet = data.split(" ")[0]
    H_inch = data.split(" ")[-1]

    H_feet_e = int(re.sub("[^0-9]", "", H_feet)) * 12
    H_inch_e = int(re.sub("[^0-9]", "", H_inch))
    to_cm = round(((H_feet_e + H_inch_e) * 2.54), 1)
    return to_cm


def lbs_to_kg(data: str):
    """
    파운드를 킬로그램으로 변환합니다.

    :param data: 변환할 데이터 문자열 (예: "170 lbs").
    :return: 변환된 킬로그램 값.
    """
    to_int = round((int(re.sub("[^0-9]", "", data)) / 2.205), 1)
    return to_int


def check_connection():
    try:
        # get_mongo_db 컨텍스트 매니저를 사용하여 MongoDB 연결 시도
        with get_mongo_db() as db:
            # 서버 상태 확인
            db.command("ping")
            print("MongoDB connection: Success")
    except errors.ServerSelectionTimeoutError as err:
        # 연결 실패시 에러 메시지
        print("MongoDB connection: Failed", err)
        logger.error(f"Error when Connection db : {err}")
        raise


def save_data(collection_name: str, data: List):

    with get_mongo_db() as mongo_db:
        try:
            mongo_db[collection_name].delete_many({})
        except Exception as e:
            logger.error(f"Error deleting fighters data: {e}")

        try:
            mongo_db[collection_name].insert_many(data)
            logger.warning(f"UFC fighters insert : {len(data)}")
        except Exception as e:
            logger.error(f"Error save fighters data: {e}")


def get_element_safe(list_, index: int = None, key: str = None):
    """
    리스트의 주어진 인덱스에서 요소를 안전하게 반환
    인덱스가 범위를 벗어나면 None을 반환
    """
    if key:
        try:
            if list_[key] == "":
                return None
            return list_[key]
        except KeyError:
            return None
    else:
        try:
            if list_[index] == "":
                return None
            return list_[index]
        except IndexError:
            return None
