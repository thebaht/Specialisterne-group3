import sys
import inspect
import requests
from pprint import pprint
from factory import Factory
import tests
import models
import random
from string import ascii_letters
from dbcontext import DatabaseContext
import sqlalchemy as sql
def getTests():
    return [(k, v) for k, v in inspect.getmembers(tests) if k.startswith("test_")]

def _sep():
    print("-"*75)

class MenuArg:
    def __init__(self, fun, arg=None):
        self._fun = fun
        self._arg = arg

    def __call__(self):
        if (self._arg):
            return self._fun(self._arg)
        else:
            return self._fun()

def _getRandom(t:type):
    """get a random value based on type"""
    if t == int:
        return random.randint(0,10000)
    if t == float:
        return random.uniform(0,1)
    if t == str:
        return "".join(random.choices(ascii_letters,k=random.randint(3,9)))
    if t == bool:
        return random.choice([True, False])
    return None # Sus
def menu_yn(question):
    return menu([("no", lambda: False),("yes", lambda : True)], preface=question)
def menu(lst: list[tuple[str, MenuArg]], preface=""):
    _sep()
    _sep()
    if preface != "":
        print(preface)
    lstStr = ""
    for i, (k, v) in enumerate(lst):
        offset = "" if i > 9 else " "
        lstStr += f"{offset}{i}) {k}\n"
    print(lstStr)
    choice = None
    while choice is None:
        try:
            choice = int(input())
        except Exception:
            print("invalid input")
    _, fun = lst[choice]
    return fun()


base_url = "http://127.0.0.1:5000"
API = base_url+"/api/item/"
API_MULTIPLE = base_url+"/api/items/"


def requestGet(multiple=False):
    endpoint = API if not multiple else API_MULTIPLE
    try:
        if not multiple:
            id = None
            while id is None:
                try:
                    id = int(input("item.id: "))
                except Exception:
                    print("Failed to parse id")
            #print(endpoint+"item/"+str(id))
            res = requests.get(endpoint+"item/"+str(id))
        else:
            table = None
            while table is None:
                try:
                    table = input("Table name: ")
                except Exception:
                    print("Invalid input")
            #print(endpoint+str(table))
            res = requests.get(endpoint+str(table),json={})
    except Exception as e:
        print(e)
    else:
        pprint(res.json())


def checkTestmode():
    endpoint = base_url+"/api/istestmode"
    try:
        res = requests.get(endpoint)
        print(res.text)
    except Exception as e:
        print(e)

def _lookupReference(table_name):
    with dbContext.get_session() as S:
        try:
            res = S.query(models.TABLES_GET(table_name).cls)
        except Exception as e:
            print(e)
            print("lookup failed")
        return(res)


def editObject(T: models.Table):
    value = {}
    done = False
    fields = [c for c in T.columns if not c.primary_key and not c.name == "type"]
    def setVal(c: models.TableColumn):
        if c.mapper is None:
            try:
                value[c.name] = c.type(input(f"enter field value ({c.type}):"))
            except:
                print("Failed to read input")
        else:
            res = _lookupReference(c.mapper)
            if res is not None:
                value[c.name] = menu([
                    (f"{row.name} id={row.id}", MenuArg(lambda x:x.id if c.type == int else c.name, arg=row))
                for row in res],preface="Pick from the list")

    def displayField(c: models.TableColumn) -> str:
        S = f"{c.name+(":? " if c.optional else ": " )+c.type.__name__:30} {" = "} {value.get(c.name, "__")}"
        if(c.mapper): S+=str(c.mapper)
        return S

    def fillWithRandom():
        for f in fields:
            if value.get(f.name) is None:
                if f.mapper is None:
                    value[f.name] = _getRandom(f.type)

    while not done:
        print(f"class: {T.name} table: {T.table}")
        _m = menu(
            [*[(displayField(c), MenuArg(setVal, arg=c))
                for c in fields],
             ("Fill empty with random data (!unpredictable!)", fillWithRandom),
             ("return", lambda: True)],
            preface="pick field to edit or return"
        )
        done = _m == True
    value["item_type"] = T.name
    return value

def _comitItemToDB(item):
    with dbContext.get_session() as S:
        S.add(item)
        S.commit()

def createItemInteractive():
    options = [(I.name, MenuArg(lambda x: x, arg=I)) for I in models.ITEMS]
    value = editObject(menu(options, preface="Pick entry type"))
    pprint(value)
    with dbContext.get_session() as S:
        try:
            item = Factory.create_item_from_dict(S,value)
        except Exception as e:
            print(e)
            print("Failed to create item")
        else:
            if(menu_yn("Comit item to database?")):
                _comitItemToDB(item)
            return item

def _make_query(tname):
    for r in _lookupReference(tname):
        _sep()
        pprint(r.__dict__)

def getMenuEntries():
    return [
        ("Check if in testmode", checkTestmode),
        ("Make get request", lambda: menu([
            ("One item", lambda: requestGet()),
            ("Multiple items", lambda: requestGet(multiple=True)),
        ])),
        ("Create new item", createItemInteractive),
        ("Make query", lambda : menu([
            (t.name, MenuArg(_make_query, arg=t.name))
        for t in models.TABLES],preface="Pick table")),
        ("Choose test", lambda: menu(getTests(), preface="Pick test")),
        ("quit", lambda: quit())
    ]

dbContext = DatabaseContext.get_instance()
if __name__ == "__main__":
    while True:
        menu(getMenuEntries())
