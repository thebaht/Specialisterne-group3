from dbcontext import *
# from itemValue import *
from sqlalchemy import update

dbcontext = DatabaseContext()
dbcontext.clear_database()

session = dbcontext.get_session()

# for game in boardGames:
#     session.add(game)






#! Just testing stuff.......................................................................
if __name__ == '__main__':
    man = Manufacturer(name="games workshop")
    man2 = Manufacturer(name="another workshop")

    fig = TabletopFigure(
        name="space marine",
        description="little space men",
        quantity=500,
        price=200.0,
        discount=0.0,
        length=2.0,
        width=1.0,
        height=3.0,
        num_units=16,
        num_pieces=600,
    )

    man.items.append(fig)
    session.add(man)
    session.add(man2)
    session.add(fig)


    manq = session.query(Manufacturer).filter(Manufacturer.name == "another workshop").first()
    fig2 = TabletopFigure(
        manufacturer=manq,
        name="some other marine",
        description="little space men",
        quantity=500,
        price=200.0,
        discount=0.0,
        length=1.0,
        width=2.0,
        height=3.0,
        num_units=16,
        num_pieces=600,
    )
    session.add(fig2)

    session.flush()
    for fig in session.query(TabletopFigure).all():
        print(f"\n{"_ "*50}\n{fig.name}")
        print(fig.manufacturer_id)
        print(f"{fig.price}\n")

    figu = session.query(TabletopFigure).filter(TabletopFigure.id == 1).first()
    figu.price = 100.0
    session.flush()

    for fig in session.query(TabletopFigure).all():
        print(f"\n{"_ "*50}\n{fig.name}")
        print(fig.discount)
        print(fig.manufacturer_id)
        print(f"{fig.price}\n")

    session.execute(update(Item).values(discount=20.0))
    session.commit()

    for fig in session.query(TabletopFigure).all():
        print(f"\n{"_ "*50}\n{fig.name}")
        print(fig.discount)
        print(fig.manufacturer_id)
        print(f"{fig.price}\n")

    session.delete(fig2)
    session.flush()

    for fig in session.query(TabletopFigure).all():
        print(f"\n{"_ "*50}\n{fig.name}")
        print(fig.manufacturer_id)
        print(f"{fig.price}\n")


    session.commit()
    session.close()
