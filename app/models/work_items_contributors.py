from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.session import Base


work_item_contributors = Table(
    'work_item_contributors',
    Base.metadata,
    Column('work_item_id', Integer, ForeignKey('work_items.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)
