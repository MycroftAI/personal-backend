from sqlalchemy import (
    Column, ForeignKey, Table,
    Integer, String, create_engine
)
from sqlalchemy.orm import (
    mapper, relationship,
    scoped_session, sessionmaker, configure_mappers
)
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy import event
import re


@event.listens_for(mapper, "mapper_configured")
def _setup_deferred_properties(mapper, class_):
    """Listen for finished mappers and apply DeferredProp
    configurations."""

    for key, value in class_.__dict__.items():
        if isinstance(value, DeferredProp):
            value._config(class_, key)


class DeferredProp(object):
    """A class attribute that generates a mapped attribute
    after mappers are configured."""

    def _setup_reverse(self, key, rel, target_cls):
        """Setup bidirectional behavior between two relationships."""

        reverse = self.kw.get('reverse')
        if reverse:
            reverse_attr = getattr(target_cls, reverse)
            if not isinstance(reverse_attr, DeferredProp):
                reverse_attr.property._add_reverse_property(key)
                rel._add_reverse_property(reverse)


class FKRelationship(DeferredProp):
    """Generates a one to many or many to one relationship."""

    def __init__(self, target, fk_col, **kw):
        self.target = target
        self.fk_col = fk_col
        self.kw = kw

    def _config(self, cls, key):
        """Create a Column with ForeignKey as well as a relationship()."""

        target_cls = cls._decl_class_registry[self.target]

        pk_target, fk_target = self._get_pk_fk(cls, target_cls)
        pk_table = pk_target.__table__
        pk_col = list(pk_table.primary_key)[0]

        if hasattr(fk_target, self.fk_col):
            fk_col = getattr(fk_target, self.fk_col)
        else:
            fk_col = Column(self.fk_col, pk_col.type, ForeignKey(pk_col))
            setattr(fk_target, self.fk_col, fk_col)

        rel = relationship(target_cls,
                           primaryjoin=fk_col == pk_col,
                           collection_class=self.kw.get('collection_class',
                                                        set)
                           )
        setattr(cls, key, rel)
        self._setup_reverse(key, rel, target_cls)


class one_to_many(FKRelationship):
    """Generates a one to many relationship."""

    def _get_pk_fk(self, cls, target_cls):
        return cls, target_cls


class many_to_one(FKRelationship):
    """Generates a many to one relationship."""

    def _get_pk_fk(self, cls, target_cls):
        return target_cls, cls


class many_to_many(DeferredProp):
    """Generates a many to many relationship."""

    def __init__(self, target, tablename, local, remote, **kw):
        self.target = target
        self.tablename = tablename
        self.local = local
        self.remote = remote
        self.kw = kw

    def _config(self, cls, key):
        """Create an association table between parent/target
        as well as a relationship()."""

        target_cls = cls._decl_class_registry[self.target]
        local_pk = list(cls.__table__.primary_key)[0]
        target_pk = list(target_cls.__table__.primary_key)[0]

        t = Table(
            self.tablename,
            cls.metadata,
            Column(self.local, ForeignKey(local_pk), primary_key=True),
            Column(self.remote, ForeignKey(target_pk), primary_key=True),
            keep_existing=True
        )
        rel = relationship(target_cls,
                           secondary=t,
                           collection_class=self.kw.get('collection_class',
                                                        set)
                           )
        setattr(cls, key, rel)
        self._setup_reverse(key, rel, target_cls)


def string(size):
    """Convenience macro, return a Column with String."""

    return Column(String(size))


def int():
    """Convenience macro, return a Column with Integer."""

    return Column(Integer)


class Base(object):
    """Base class which auto-generates tablename, surrogate
    primary key column.

    Also includes a scoped session and a database generator.

    """

    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase class name to underscores_between_words
        table name."""
        name = cls.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m: "_" + m.group(0).lower(), name[1:])
        )

    id = Column(Integer, primary_key=True)
    """Surrogate 'id' primary key column."""

    @classmethod
    def setup_database(cls, url, create=False, echo=False):
        """'Setup everything' method for the ultra lazy."""

        configure_mappers()
        e = create_engine(url, echo=echo)
        if create:
            cls.metadata.create_all(e)
        cls.session = scoped_session(sessionmaker(e))


MagicBase = declarative_base(cls=Base)

if __name__ == '__main__':

    class Parent(MagicBase):
        children = one_to_many("Child", "child_id",
                               reverse="parent")


    class Child(MagicBase):
        parent = many_to_one("Parent", "child_id",
                             reverse="children")

        tags = many_to_many("Tag", "child_tag",
                            "child_id",
                            "tag_id")


    class Tag(MagicBase):
        name = string(50)


    MagicBase.setup_database("sqlite://", create=True, echo=True)

    t1, t2, t3 = Tag(name='t1'), Tag(name='t2'), Tag(name='t3')
    MagicBase.session.add(Parent(
        children={
            Child(tags={t1, t2}),
            Child(tags={t1, t3}),
            Child()
        }))
    MagicBase.session.commit()

    p1 = MagicBase.session.query(Parent).first()
    for child in p1.children:
        print child, [t.name for t in child.tags]