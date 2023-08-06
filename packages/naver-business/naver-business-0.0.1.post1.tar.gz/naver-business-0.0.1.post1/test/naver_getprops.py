import naver_dbcore as nvr

p = nvr.Persistence()

if __name__ == '__main__': 
    res = p.getProps("user")
    print (res)