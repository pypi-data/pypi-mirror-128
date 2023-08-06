
Extend Object Code
==================

Pip:https://pypi.org/project/exobject


^^^^^^^^
Expamle:
^^^^^^^^
    ::

        from ExObject.ExObject import ExObject
        from ExObject.DateTime import DateTime
        a=ExObject([
            {"name":"a","age":1},
            {"name":"b","age":51},
            {"name":"c","age":11},
            {"name":"d","age":22}
        ])
        b=a.SortBy(lambda x:x["age"],True)
        print(b)
        #====
        b=a.SortBy(lambda x:x["age"],False)
        print(b)
        #====
        print(a.Select(lambda x:x["name"].ToString()))
        c=a.Where(lambda x:x["age"]<10).FirstOrDefaultObject()
        print(c)
        print(c["?name"].ToString())#print a
        print(c["?nickName"].ToString())#print none
        #====
        date=DateTime.Now()
        date2=DateTime.AutoConvert("2019-02-06")
        print(date2)
