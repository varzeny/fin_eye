# nasdaq_data_link.py

# lib
import nasdaqdatalink

# module


#definition
class NasdaqDataLink:
    is_active = False

    @classmethod
    def activate(cls, data:dict):
        if cls.is_active:print("already activated");return False

        nasdaqdatalink.ApiConfig.api_key = data["key"]
        cls.is_active = True
        print("activate!")


    @classmethod
    def deactivate(cls):
        if not cls.is_active:print("already deactivated!");return False

        cls.is_active = False   
        print("deactivate!")


    @classmethod
    def get_data_from_api(cls, tbl:str, start_date, end_date):
        if not cls.is_active:print("not activate!");return False

        try:
            data = nasdaqdatalink.get(
                tbl, 
                start_date=start_date, 
                end_date=end_date
            )
            return data
        except Exception as e:
            print("error! : ",e)
            return False



# "FRED/DEXUSEU","FRED/DEXCHUS","FRED/DEXINUS","FRED/DEXJPUS","FRED/DEXKOUS"



# @router.get("/test1")
# async def get_test1( ss:AsyncSession=Depends( DB.get_ss ) ):
#     print("!!!")

    
#     source="FRED"
#     target="DEX"
#     currency="KOUS"

#     result = NasdaqDataLink.get_data_from_api(
#         tbl = f"{source}/{target}{currency}",
#         start_date="",
#         end_date=""
#     )

#     query = """
#     INSERT INTO exchange_rate(day, currency, rate, source)
#     VALUES(:day, :currency, :rate, :source) AS vals
#     ON DUPLICATE KEY UPDATE rate=vals.rate, source=vals.source;    
#     """

#     for i, r in result.itertuples():
#         await ss.execute(
#             statement=text(query),
#             params={
#                 "day":i,
#                 "currency":currency,
#                 "rate":r,
#                 "source":source
#             }
#         )
#     await ss.commit()
#     print("test1 완료!")
