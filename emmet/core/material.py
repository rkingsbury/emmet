""" Core definition of a Materials Document """
from typing import List, Dict
from datetime import datetime

from pydantic import BaseModel, Field

from emmet.stubs.pymatgen import Structure
from emmet.core.structure import StructureMetadata


class PropertyOrigin(BaseModel):
    """
    Provenance document for the origin of properties in a material document
    """

    property: str = Field(..., description="The materials document property")
    task_type: str = Field(
        ..., description="The original calculation type this propeprty comes from"
    )
    task_id: str = Field(..., description="The calculation ID this property comes from")
    last_update: datetime = Field(
        ..., description="The timestamp when this calculation was last updated"
    )


class MaterialsDoc(BaseModel, StructureMetadata):
    """
    Definition for a full Materials Document
    Subsections can be defined by other builders
    """

    structure: Structure = Field(
        None, description="The best structure for this material"
    )

    initial_structures: List[Structure] = Field(
        list(),
        description="Initial structures used in the DFT optimizations corresponding to this material",
    )

    task_ids: List[str] = Field(
        [],
        title="Calculation IDs",
        description="List of Calculations IDs used to make this Materials Document",
    )

    deprecated_tasks: List[str] = Field([], title="Deprecated Tasks")

    deprecated: bool = Field(
        None,
        description="Whether this materials document is deprecated due to a lack of high enough quality calculation.",
    )

    # Only material_id is required for all documents
    material_id: str = Field(
        ...,
        description="The ID of this material, used as a universal reference across proeprty documents."
        "This comes in the form: mp-******",
    )

    last_updated: datetime = Field(
        None,
        description="Timestamp for the most recent calculation for this Material document",
    )
    created_at: datetime = Field(
        None,
        description="Timestamp for the first calculation for this Material document",
    )
    task_types: Dict[str, str] = Field(
        {},
        description="Calculation types for all the calculations that make up this material",
    )

    origins: List[PropertyOrigin] = Field(
        [], description="Dictionary for tracking the provenance of properties"
    )

    @classmethod
    def build(cls, structure: Structure, material_id: str, **kwargs) -> "MaterialsDoc":
        """
        Builds a materials document using the minimal amount of information
        """
        meta = StructureMetadata.from_structure(structure)
        kwargs.update(**meta.dict())

        if "last_updated" not in kwargs:
            kwargs["last_updated"] = datetime.utcnow()

        if "created_at" not in kwargs:
            kwargs["created_at"] = datetime.utcnow()

        return cls(material_id=material_id, **kwargs)