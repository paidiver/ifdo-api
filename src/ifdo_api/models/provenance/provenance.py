from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.image_set import image_set_provenance_activities
from ifdo_api.models.image_set import image_set_provenance_agents
from ifdo_api.models.image_set import image_set_provenance_entities

# Association tables for many-to-many relationships
provenanceentity_agent = Table(
    "provenanceentity_agent",
    Base.metadata,
    Column("entity_id", ForeignKey("provenance_entities.id"), primary_key=True),
    Column("agent_id", ForeignKey("provenance_agents.id"), primary_key=True),
)

provenanceentity_activity = Table(
    "provenanceentity_activity",
    Base.metadata,
    Column("entity_id", ForeignKey("provenance_entities.id"), primary_key=True),
    Column("activity_id", ForeignKey("provenance_activities.id"), primary_key=True),
)

provenanceactivity_agent = Table(
    "provenanceactivity_agent",
    Base.metadata,
    Column("activity_id", ForeignKey("provenance_activities.id"), primary_key=True),
    Column("agent_id", ForeignKey("provenance_agents.id"), primary_key=True),
)

provenanceactivity_entity = Table(
    "provenanceactivity_entity",
    Base.metadata,
    Column("activity_id", ForeignKey("provenance_activities.id"), primary_key=True),
    Column("entity_id", ForeignKey("provenance_entities.id"), primary_key=True),
)


class ProvenanceAgent(DefaultColumns, Base):
    """Represents an agent in the provenance model."""

    __tablename__ = "provenance_agents"

    name = Column(String(255), nullable=False, info={"help_text": "A human-readable identifier of the agent"})
    unique_id = Column(String(500), unique=True, nullable=False, info={"help_text": "A unique identifier for the agent. Could be a URI."})

    image_sets = relationship("ImageSet", secondary=image_set_provenance_agents, back_populates="provenance_agents")

    def __str__(self):
        return self.name


class ProvenanceEntity(DefaultColumns, Base):
    """Represents an entity in the provenance model."""

    __tablename__ = "provenance_entities"

    name = Column(String(255), nullable=False, info={"help_text": "A human-readable identifier of the entity"})
    unique_id = Column(String(500), unique=True, nullable=False, info={"help_text": "A unique identifier for the entity. Could be a URI."})
    created_at = Column(DateTime, nullable=True, info={"help_text": "The time at which this entity was created in its entirety"})

    attributed_to = relationship(
        "ProvenanceAgent",
        secondary=provenanceentity_agent,
        backref="provenance_entities",
        info={"help_text": "A list of agents that relate to this entity"},
    )

    generated_by = relationship(
        "ProvenanceActivity",
        secondary=provenanceentity_activity,
        backref="generated_entities",
        info={"help_text": "A list of activities that created this entity"},
    )

    image_sets = relationship("ImageSet", secondary=image_set_provenance_entities, back_populates="provenance_entities")

    def __str__(self):
        return self.name


class ProvenanceActivity(DefaultColumns, Base):
    """Represents an activity in the provenance model."""

    __tablename__ = "provenance_activities"

    start_time = Column(DateTime, nullable=True, info={"help_text": "The time at which the activity began"})
    end_time = Column(DateTime, nullable=True, info={"help_text": "The time at which the activity ended"})

    associated_agents = relationship(
        "ProvenanceAgent",
        secondary=provenanceactivity_agent,
        backref="provenance_activities",
        info={"help_text": "The agents that are associated to this activity"},
    )

    used_entities = relationship(
        "ProvenanceEntity",
        secondary=provenanceactivity_entity,
        backref="used_in_activities",
        info={"help_text": "The entities that are associated to this activity"},
    )

    image_sets = relationship("ImageSet", secondary=image_set_provenance_activities, back_populates="provenance_activities")

    def __str__(self):
        start = self.start_time.isoformat() if self.start_time else "unknown start"
        end = self.end_time.isoformat() if self.end_time else "unknown end"
        return f"Activity from {start} to {end}"
