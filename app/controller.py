# controller.py

## lib
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

## module
from app.core.database_manager import DatabaseManager as DB
from app.service.financial_modeling_prep import FinancialModelingPrep

## definition
router = APIRouter()
template = Jinja2Templates(directory="app/template")




## definition
### test
@router.get("/get_index")
async def get_index( ss:AsyncSession=Depends( DB.get_ss ) ):
    print("get_index 시작")

    result = FinancialModelingPrep.get_index_by_name("index")
    print(result)

    print("get_index 종료")
    


@router.get("/get_forex6")
async def get_test1( ss:AsyncSession=Depends( DB.get_ss ) ):
    print( "get_forex6 시작" )
    
    query = """
    SELECT date_, pair, c4ya FROM forex;
    """
    result = await ss.execute( text(query) )
    data = [ {"date":row[0].isoformat(), "pair":row[1], "rate":row[2]} for row in result.fetchall() ]

    print( "get_forex6 완료" )
    return JSONResponse( content={"data":data}, status_code=200 )


@router.get("/make_forex_c4ya")
async def get_test1( ss:AsyncSession=Depends( DB.get_ss ) ):
    print( "make_forex_c4ya 시작" )

    query = """
    UPDATE forex f1
    JOIN (
        SELECT 
            f2.date_,
            f2.pair,
            (SELECT AVG(f3.rate) 
            FROM forex f3 
            WHERE f3.pair = f2.pair AND f3.date_ BETWEEN DATE_SUB(f2.date_, INTERVAL 4 YEAR) AND f2.date_
            ) AS avg_rate
        FROM forex f2
    ) f_avg
    ON f1.date_ = f_avg.date_ AND f1.pair = f_avg.pair
    SET f1.c4ya = ((f1.rate - f_avg.avg_rate) / f_avg.avg_rate) * 100;
    """

    await ss.execute( statement=text(query) )
    await ss.commit()

    print( "make_forex_c4ya 완료" )


@router.get("/get_forex6_from_FMP")
async def get_forex6_from_FMP( ss:AsyncSession=Depends( DB.get_ss ) ):
    print("get_forex6_from_FMP 시작!")

    query = """
    INSERT INTO forex(day, pair, source, rate)
    VALUES(:day, :pair, :source, :rate) AS vals
    ON DUPLICATE KEY UPDATE rate=vals.rate    
    """

    for p in FinancialModelingPrep.forex_list:
        result = FinancialModelingPrep.get_forex_by_pair( p )

        for row in result["historical"]:
            await ss.execute(
                statement=text( query ),
                params={
                    "day":row["date"],
                    "pair":p,
                    "source":"FMP",
                    "rate":row["close"]
                }
            )
        await ss.commit() 
    print("get_forex6_from_FMP 완료!")



### navigation
@router.get("/")
async def get_root( req:Request ):
    return template.TemplateResponse( "fin_eye.html", { "request":req } )


