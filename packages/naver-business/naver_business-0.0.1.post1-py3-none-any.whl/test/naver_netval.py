import naver_dbcore as nvr

p = nvr.Persistence()

if __name__ == '__main__':
    try:
        res = p.getNextVal('id_tournament','tournament')
        print(res)
    except Exception as e:
        print("ERROR")
        pass
