from datetime import datetime
from pydantic import BaseModel
from pydantic import Field


class ProvenanceAgentSchema(BaseModel):
    """Someone or something responsible for conducting an activity."""

    name: str = Field(..., max_length=255, description="A human-readable identifier of the agent")
    unique_id: str = Field(..., max_length=500, description="A unique identifier for the agent. Could be a URI.")


class ProvenanceEntitySchema(BaseModel):
    """A static instance of a virtual thing."""

    name: str = Field(..., max_length=255, description="A human-readable identifier of the entity")
    unique_id: str = Field(..., max_length=500, description="A unique identifier for the entity. Could be a URI.")
    created_at: datetime | None = Field(None, description="The time at which this entity was created in its entirety")
    attributed_to: list[ProvenanceAgentSchema] | None = Field(default_factory=list, description="Agents related to this entity")
    generated_by: list["ProvenanceActivitySchema"] | None = Field(default_factory=list, description="Activities that created this entity")


class ProvenanceActivitySchema(BaseModel):
    """A process that works with entities and is operated by agents."""

    start_time: datetime | None = Field(None, description="The time at which the activity began")
    end_time: datetime | None = Field(None, description="The time at which the activity ended")
    associated_agents: list[ProvenanceAgentSchema] | None = Field(default_factory=list, description="Agents associated with this activity")
    used_entities: list[ProvenanceEntitySchema] | None = Field(default_factory=list, description="Entities associated with this activity")


ProvenanceEntitySchema.model_rebuild()
ProvenanceActivitySchema.model_rebuild()
