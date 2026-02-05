from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue, 
    DictElement, 
    Dictionary, 
    Float, 
    LevelDirection, 
    SimpleLevels
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form():
    return Dictionary(
        elements={
            "cpu_levels_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for CPU utilization"),
                    form_spec_template=Float(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(80.0, 90.0)),
                ),
                required=False,
            ),
            "cpu_levels_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels for CPU utilization"),
                    form_spec_template=Float(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue(value=(10.0, 5.0)),
                ),
                required=False,
            ),
        }
    )


rule_spec_ruckus_cpu = CheckParameters(
    name="ruckus_cpu",
    title=Title("Ruckus CPU Utilization"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_form,
    condition=HostCondition(),
)
