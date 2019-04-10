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

    note = db.Column(db.String)

    __table_args__ = (
        db.UniqueConstraint('lsh',
                            'clid',
                            name='we_are_special'),
    )

    def __repr__(self):
        return '<AmbulManage %r>' % self.id

    def display(self):
        return {}


class AmbulManagePictures(db.Model):
    __tablename__ = 'ambul_manage_pictures'
    id = db.Column(SLBigInteger, primary_key=True)
    ambul_manage_id = db.Column(
        SLBigInteger,
        db.ForeignKey('ambul_manage.id', ondelete='CASCADE'),
        nullable=False)
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
