from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns


class Label(DefaultColumns, Base):
    """A semantic label that can be assigned to an annotation."""

    __tablename__ = "labels"
    name = Column(
        String(255),
        nullable=False,
        unique=True,
        info={"help": "A human-readable name for the semantic label"},
    )
    parent_id = Column(
        ForeignKey("labels.id"),
        nullable=True,
        info={"help": "The ID of the parent label, if any"},
    )

    label_source_id = Column(
        ForeignKey("label_sources.id"),
        nullable=True,
        info={"help": "The ID of the source from which this label originates"},
    )
    info = Column(
        Text,
        nullable=True,
        info={"help": "A description on what this semantic label represents"},
    )

    parent = relationship("Label", remote_side=[DefaultColumns.id], backref="children")


class LabelSource(DefaultColumns, Base):
    """A source or ontology from which labels are derived."""

    __tablename__ = "label_sources"
    name = Column(
        String(255),
        nullable=False,
        unique=True,
        info={"help": "A human-readable name for the label source"},
    )
    description = Column(
        Text,
        nullable=True,
        info={"help": "A description of the label source or ontology"},
    )
