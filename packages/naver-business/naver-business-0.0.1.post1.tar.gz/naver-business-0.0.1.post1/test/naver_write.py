import naver_dbcore as nvr

p = nvr.Persistence()

if __name__ == '__main__':
    try:
        stm="""INSERT INTO GAMER VALUES(7777,'gamer9','jose','cuevas','jose@aol.com',123456,1,1,4)"""
        res = p.setWrite(stm,"GAMER")
        cursor = res["cursor"]
        session = res["session"]
        print("AQUI")
        session.commit()
        print (cursor.lastrowid)
    except Exception as e:
        print("ERROR")
        pass
