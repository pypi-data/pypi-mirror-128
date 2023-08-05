"""
Special requirement and candidate classes to describe a requires-python constraint
"""

from typing import Iterable, Iterator, Mapping, cast

from pdm import termui
from pdm.models.candidates import Candidate
from pdm.models.environment import Environment
from pdm.models.requirements import NamedRequirement, Requirement
from pdm.models.specifiers import PySpecSet


class PythonCandidate(Candidate):
    def format(self) -> str:
        return (
            f"{termui.green(self.name, bold=True)} "
            f"{termui.yellow(str(self.req.specifier))}"
        )


class PythonRequirement(NamedRequirement):
    @classmethod
    def from_pyspec_set(cls, spec: PySpecSet) -> "PythonRequirement":
        return cls(name="python", specifier=spec)

    def as_candidate(self, environment: Environment) -> PythonCandidate:
        return PythonCandidate(self, environment)


def find_python_matches(
    identifier: str,
    requirements: Mapping[str, Iterator[Requirement]],
    environment: Environment,
) -> Iterable[Candidate]:
    """All requires-python except for the first one(must come from the project)
    must be superset of the first one.
    """
    python_reqs = cast(Iterator[PythonRequirement], iter(requirements[identifier]))
    project_req = next(python_reqs)
    python_specs = cast(Iterator[PySpecSet], (req.specifier for req in python_reqs))
    if all(spec.is_superset(project_req.specifier or "") for spec in python_specs):
        return [project_req.as_candidate(environment)]
    else:
        # There is a conflict, no match is found.
        return []


def is_python_satisfied_by(requirement: Requirement, candidate: Candidate) -> bool:
    return cast(PySpecSet, requirement.specifier).is_superset(candidate.req.specifier)
