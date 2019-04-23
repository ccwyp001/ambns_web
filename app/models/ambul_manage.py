# -*- coding: utf-8 -*-

from ..extensions import db, SLBigInteger


class AmbulManage(db.Model):
    __tablename__ = 'ambul_manage'
    id = db.Column(SLBigInteger, primary_key=True)
    lsh = db.Column(db.String(100))
    clid = db.Column(db.String(100))

    is_workwear = db.Column(db.Integer)
    is_wear_work_cards = db.Column(db.Integer)
    is_take_medical_warehouse = db.Column(db.Integer)

    note = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint('lsh',
                            'clid',
                            name='we_are_special'),
    )

    def __repr__(self):
        return '<AmbulManage %r>' % self.id

    def display(self):
        return {'fileList': [_.display() for _ in self.pictures.all()],
                'registered': True,
                'desc': self.note,
                'workwear': [str(_) for _ in [1,2,4] if _ & self.is_workwear] ,
                'work_cards': [str(_) for _ in [1,2,4] if _ & self.is_wear_work_cards],
                'medical_warehouse': [str(_) for _ in [1,2,4] if _ & self.is_take_medical_warehouse],
                }

    @classmethod
    def from_data(cls, data):
        lsh = data.get('lsh')
        clid = data.get('clid')
        workwear = data.get('workwear')
        workwear = sum([int(_) for _ in workwear])
        desc = data.get('desc')
        work_cards = data.get('work_cards')
        work_cards = sum([int(_) for _ in work_cards])
        medical_warehouse = data.get('medical_warehouse')
        medical_warehouse = sum([int(_) for _ in medical_warehouse])
        return AmbulManage(
            lsh=lsh,
            clid=clid,
            is_workwear=workwear,
            is_wear_work_cards=work_cards,
            is_take_medical_warehouse=medical_warehouse,
            note=desc
        )


class AmbulManagePictures(db.Model):
    __tablename__ = 'ambul_manage_pictures'
    id = db.Column(SLBigInteger, primary_key=True)
    ambul_manage_id = db.Column(
        SLBigInteger,
        db.ForeignKey('ambul_manage.id', ondelete='CASCADE'),
        nullable=True)
    ambul_manage = db.relationship(
        'AmbulManage',
        backref=db.backref('pictures', cascade="delete", lazy='dynamic'))

    name = db.Column(db.String(100))
    url = db.Column(db.String(100))
    thumb_text = db.Column(db.Text)

    def __repr__(self):
        return '<AmbulManagePictures %r>' % self.id

    def display(self):
        return {'thumbUrl': self.thumb_text,
                'name': self.name,
                'uid': self.id
                }

    @classmethod
    def from_data(cls, data):
        name = data.get('name')
        thumb_text = data.get('thumbUrl')

        return AmbulManagePictures(
            name=name,
            thumb_text=thumb_text
        )