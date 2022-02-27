from models import User, Category, Pack, Card
from uuid import uuid4

def create_package(db,form):
    # form = dict(request.form)
    category = Category.query.filter_by(name=form["category"]).first()
    if not category:
        cat_id = uuid4().hex
        category = Category(id=cat_id,name=form["category"])

    pack_id = uuid4().hex
    new_pack = Pack(id=pack_id,name=form["pack_name"],id_category=category.id,id_user=form["id_user"])

    side_a = [v for k,v in form.items() if k.find("side") >= 0 and k.find("a") >= 0]
    side_b = [v for k,v in form.items() if k.find("side") >= 0 and k.find("b") >= 0]

    for element in zip(side_a,side_b):
        car_id = uuid4().hex
        new_card = Card(id=car_id,side_a=element[0],side_b=element[1],id_pack=new_pack.id)
        db.session.add(new_card)

    db.session.add(category)
    db.session.add(new_pack)
    db.session.commit()
    return True