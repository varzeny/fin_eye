# database_manager.py

# lib
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# definition
Base = declarative_base()
class BaseModel(Base):
    __abstract__=True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class DatabaseManager:
    base = BaseModel
    is_active = False
    db_url = None
    async_engine = None
    async_session = None


    @classmethod
    def activate( cls, data:dict ):
        # 이미 기종 중이면
        if cls.is_active:print("이미 기동 중!");return False
        # 세팅
        cls.db_url = data["db_url"]
        cls.async_engine = create_async_engine(
            url=cls.db_url,
            pool_size=10
        )
        cls.async_session = sessionmaker(
            bind=cls.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        cls.is_active = True
        print("DB 기동 완료 !")
        return True
    

    @classmethod
    async def deactivate(cls):
        # 기동중이 아니면
        if not cls.is_active:print("DB는 기동중이 아님!");return False
        # 종료
        await cls.async_engine.dispose()
        cls.async_engine = None
        cls.async_session = None
        cls.is_active = False
        print("DB 종료 완료 !")


    @classmethod
    async def get_ss(cls):
        try:
            ss = cls.async_session()
            yield ss
        except Exception as e:
            print("error : ",e)
            await ss.rollback()
        finally:
            await ss.close()
