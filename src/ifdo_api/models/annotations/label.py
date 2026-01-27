from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
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
        info={"help": "Name in BIIGLE label tree output; name of label as annotated"},
    )

    parent_label_name = Column(
        String(255),
        nullable=False,
        info={"help": "Name of parent to label_name"},
    )

    lowest_taxonomic_name = Column(
        String(255),
        nullable=True,
        info={"help": "Most detailed taxonomic identification possible; scientificName field in DarwinCore"},
    )

    lowest_aphia_id = Column(
        String(50),
        nullable=True,
        info={"help": "The AphiaID corresponding to the lowest_taxonomic_name, if applicable"},
    )

    name_is_lowest = Column(
        Boolean,
        nullable=False,
        default=False,
        info={"help": "Indicates whether the name field represents the lowest taxonomic identification"},
    )

    identification_qualifier = Column(
        String(255),
        nullable=True,
        info={"help": "Open nomenclature signs (see Horton et al 2021); same field name in DarwinCore"},
    )

    annotation_set_id = Column(
        ForeignKey("annotation_sets.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        info={"help_text": "The annotation_set this label belongs to. A annotation_set can have multiple labels."},
    )

    annotation_set = relationship(
        "AnnotationSet",
        back_populates="labels",
        info={"help_text": "Annotation sets that include this label"},
        passive_deletes=True,
    )

    # label_source_id = Column(
    #     ForeignKey("label_sources.id"),
    #     nullable=True,
    #     info={"help": "The ID of the source from which this label originates"},
    # )
    # parent_id = Column(
    #     ForeignKey("labels.id"),
    #     nullable=True,
    #     info={"help": "The ID of the parent label, if any"},
    # )
    # parent = relationship(
    #     "Label",
    #     remote_side="Label.id",
    #     foreign_keys=[parent_id],
    #     back_populates="childrens",
    # )
    # childrens = relationship(
    #     "Label",
    #     foreign_keys=[parent_id],
    #     back_populates="parent",
    #     cascade="all, delete-orphan",
    # )


# class LabelSource(DefaultColumns, Base):
#     """A source or ontology from which labels are derived."""

#     __tablename__ = "label_sources"
#     name = Column(
#         String(255),
#         nullable=False,
#         unique=True,
#         info={"help": "A human-readable name for the label source"},
#     )
#     description = Column(
#         Text,
#         nullable=True,
#         info={"help": "A description of the label source or ontology"},
#     )
