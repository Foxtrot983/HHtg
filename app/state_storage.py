from typing import Dict, Any

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from .models import Session, FSMRecord


class SqlAlchemyStorage(BaseStorage):

    async def wait_closed(self):
        pass

    async def close(self):
        pass

    async def get_state(self, key: StorageKey) -> str | None:
        with Session() as session:
            record = session.query(FSMRecord).filter_by(chat_id=key.chat_id, user_id=key.user_id).first()
            if record is None:
                return key.destiny
            return record.state or key.destiny
    
    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        with Session() as session:
            record = session.query(FSMRecord).filter_by(chat_id=key.chat_id, user_id=key.user_id).first()
            if record is None:
                return dict()
            return record.data or dict()
    
    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        with Session() as session:
            if row := session.query(FSMRecord).filter_by(chat_id=key.chat_id, user_id=key.user_id).first():
                if data:
                    row.data = data
            else:
                row = FSMRecord(chat_id=key.chat_id, user_id=key.user_id, data=data)
                session.add(row)
            session.commit()
    
    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        with Session() as session:
            if row := session.query(FSMRecord).filter_by(chat_id=key.chat_id, user_id=key.user_id).first():
                row.state = state.state if state else None
            else:
                row = FSMRecord(chat_id=key.chat_id, user_id=key.user_id, state=state.state if state else None)
                session.add(row)
            session.commit()