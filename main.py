# main.py

# lib
import os
from fastapi import FastAPI, staticfiles

# module
from app.core.util_manager import read_file_for_json
from app.core.database_manager import DatabaseManager
from app.service.financial_modeling_prep import FinancialModelingPrep
from app.controller import router

# definition
def startup_sequence():
    print("app 기동 중...")
    # read config
    app.state.config = read_file_for_json( os.path.dirname(__file__) + "/config.json" )

    # db setup
    DatabaseManager.activate( app.state.config["db"] )

    # financial_modiling_prep setup
    FinancialModelingPrep.activate( app.state.config["api"]["financial_modeling_prep"] )

    # static 마운트
    app.mount(
        path="/static",
        app=staticfiles.StaticFiles(directory="app/static"),
        name="static"
    )

    # 앤드포인트 라우터
    app.include_router( router )

    print("app 기동 완료 !")


async def shutdown_sequence():
    print("app 종료 중...")
    # db shutdown
    await DatabaseManager.deactivate()

    print("app 종료 완료 !")


app = FastAPI(
    on_startup=[
        startup_sequence
    ],
    on_shutdown=[
        shutdown_sequence
    ]
)




if __name__ == "__main__":
    print()
    