import sys
import inspect
import requests
from pprint import pprint
import tests
import models


def getTests():
    return [(k, v) for k, v in inspect.getmembers(tests) if k.startswith("test_")]


def menu(lst: list[tuple[str, any]], preface=""):
    if preface != "":
        print(preface)
    lstStr = ""
    for i, (k, v) in enumerate(lst):
        lstStr += f"{i}) {k}\n"
    print(lstStr)
    choice = None
    while choice is None:
        try:
            choice = int(input())
        except Exception:
            print("invalid input")
    pprint(lst[choice])
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
            res = requests.get(endpoint+"item/"+str(id))
        else:
            table = None
            while table is None:
                try:
                    table = input("Table name: ")
                except Exception:
                    print("Invalid input")
            res = requests.get(endpoint+str(table))
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

def editObject(T: models.Table):
    print(T.name)
    value = {}
    done = False
    options = [
        *[(c.name, lambda: pprint(c.name)) for c in T.columns],
        ("return", lambda: True)
    ]
    while not done:
        print(f"class: {T.name} table: {T.table}")
        print(done)
        _m = menu(options,preface="pick field to edit or return")
        done = _m == True
    return value
def createItemInteractive():
    table = None
    items = [x for x in models.TABLES]
    options = [(I.name, lambda : i) for i,I in enumerate(items)]
    choice = menu(options, preface="Pick entry type")
    print("Picked entry type")
    pprint(choice)
    editObject(items[choice])
    pprint(items)


def getMenuEntries():
    return [
        ("Check if in testmode", checkTestmode),
        ("Make get request", lambda: menu([
            ("One item", lambda: requestGet()),
            ("Multiple items", lambda: requestGet(multiple=True)),
        ])),
        ("Create new item", createItemInteractive),
        ("Choose test", lambda: menu(getTests(), preface="Pick test")),
        ("quit", lambda: quit())
    ]


if __name__ == "__main__":
    while True:
        menu(getMenuEntries())
