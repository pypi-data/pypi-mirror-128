import naver_dbcore as nvr

p = nvr.Persistence()

if __name__ == '__main__':
    stm="""SELECT * from GAMER where identification='1758725269'"""
    res = p.getQuery(stm,"GAMER")
    print (res)