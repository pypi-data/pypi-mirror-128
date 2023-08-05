from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AlgoExecutionDataTargetpredictionslowerbound")


@attr.s(auto_attribs=True)
class AlgoExecutionDataTargetpredictionslowerbound:
    """ Prediction Lower bounds by Horizon for each target. Keys are target names. Values are prediction lower bounds. """

    additional_properties: Dict[str, float] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        algo_execution_data_targetpredictionslowerbound = cls()

        algo_execution_data_targetpredictionslowerbound.additional_properties = d
        return algo_execution_data_targetpredictionslowerbound

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> float:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: float) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
