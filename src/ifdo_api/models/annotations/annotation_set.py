from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.common_fields import CommonFieldsAll

annotation_set_creators = Table(
    "annotation_set_creators",
    Base.metadata,
    Column("annotation_id", ForeignKey("annotations.id", ondelete="CASCADE"), primary_key=True),
    Column("creator_id", ForeignKey("creators.id", ondelete="CASCADE"), primary_key=True),
)


annotation_set_image_sets = Table(
    "annotation_set_image_sets",
    Base.metadata,
    Column("annotation_id", ForeignKey("annotations.id", ondelete="CASCADE"), primary_key=True),
    Column("image_set_id", ForeignKey("image_sets.id", ondelete="CASCADE"), primary_key=True),
)


class AnnotationSet(CommonFieldsAll, DefaultColumns, Base):
    """A collection of annotations that are related to a specific project, event, or context."""

    __tablename__ = "annotation_sets"
    context_id = Column(
        ForeignKey("contexts.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The overarching project context within which the annotation set was created"},
    )
    project_id = Column(
        ForeignKey("projects.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The more specific project or expedition or cruise or experiment or ... within which the annotation set was created."},
    )
    pi_id = Column(
        ForeignKey("pis.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the principal investigator of the annotation set"},
    )
    license_id = Column(
        ForeignKey("licenses.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to the license to use the data (should be FAIR, e.g. **CC-BY** or CC-0)"},
    )

    context = relationship("Context", foreign_keys=[context_id], back_populates="annotations", passive_deletes=True)
    project = relationship("Project", foreign_keys=[project_id], back_populates="annotations", passive_deletes=True)
    pi = relationship("PI", foreign_keys=[pi_id], back_populates="annotations", passive_deletes=True)
    license = relationship("License", foreign_keys=[license_id], back_populates="annotations", passive_deletes=True)

    creators = relationship(
        "Creator",
        secondary=annotation_set_creators,
        back_populates="annotations",
        info={"help_text": "Information to identify the creators of the annotation set"},
    )

    version = Column(
        String(50),
        nullable=True,
        info={"help_text": ("The version of the annotation set.")},
    )

    image_sets = relationship(
        "ImageSet",
        secondary=annotation_set_image_sets,
        back_populates="annotation_sets",
        info={"help_text": "Relationship to image_sets included in this annotation set."},
    )

    annotations = relationship(
        "Annotation",
        back_populates="annotation_sets",
        cascade="all, delete-orphan",
        info={"help_text": "The annotations that are part of this annotation set."},
    )

    labels = relationship(
        "Label",
        back_populates="annotation_sets",
        cascade="all, delete-orphan",
        info={"help_text": "The labels that are part of this annotation set."},
    )
