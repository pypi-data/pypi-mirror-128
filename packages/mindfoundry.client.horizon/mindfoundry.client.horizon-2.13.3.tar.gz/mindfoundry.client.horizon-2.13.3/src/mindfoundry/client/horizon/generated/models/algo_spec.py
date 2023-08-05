from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.trading_algo_param_spec import TradingAlgoParamSpec
from ..types import UNSET, Unset

T = TypeVar("T", bound="AlgoSpec")


@attr.s(auto_attribs=True)
class AlgoSpec:
    """ Contains the properties required to create/update an Algo  """

    code: str
    parameters_spec: List[TradingAlgoParamSpec]
    name: Union[Unset, str] = "New Algo"
    description: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        parameters_spec = []
        for parameters_spec_item_data in self.parameters_spec:
            parameters_spec_item = parameters_spec_item_data.to_dict()

            parameters_spec.append(parameters_spec_item)

        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "parametersSpec": parameters_spec,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        parameters_spec = []
        _parameters_spec = d.pop("parametersSpec")
        for parameters_spec_item_data in _parameters_spec:
            parameters_spec_item = TradingAlgoParamSpec.from_dict(parameters_spec_item_data)

            parameters_spec.append(parameters_spec_item)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        algo_spec = cls(
            code=code,
            parameters_spec=parameters_spec,
            name=name,
            description=description,
        )

        algo_spec.additional_properties = d
        return algo_spec

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
