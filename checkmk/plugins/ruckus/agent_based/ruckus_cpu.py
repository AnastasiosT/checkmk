#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    startswith,
    check_levels,
)


def parse_ruckus_cpu(string_table: StringTable) -> dict:
    """Parse the CPU utilization data"""
    parsed = {}
    if string_table:
        cpu_data = string_table[0]
        if len(cpu_data) >= 4:
            parsed = {
                "cpu_1s": int(cpu_data[0]) if cpu_data[0].isdigit() else 0,
                "cpu_5s": int(cpu_data[1]) if cpu_data[1].isdigit() else 0,
                "cpu_60s": int(cpu_data[2]) if cpu_data[2].isdigit() else 0,
                "cpu_300s": int(cpu_data[3]) if cpu_data[3].isdigit() else 0,
            }
    return parsed


def inventory_ruckus_cpu(section: dict) -> DiscoveryResult:
    """Discover CPU service if data is available"""
    if section:
        yield Service()


def check_ruckus_cpu(params: dict, section: dict) -> CheckResult:
    """Check CPU utilization levels"""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No CPU data available")
        return

    cpu_1s = section.get("cpu_1s", 0)
    cpu_5s = section.get("cpu_5s", 0)
    cpu_60s = section.get("cpu_60s", 0)
    cpu_300s = section.get("cpu_300s", 0)

    # Primary check on 5s average using check_levels()
    yield from check_levels(
        cpu_5s,
        levels_upper=params.get("cpu_levels_upper"),
        levels_lower=params.get("cpu_levels_lower"),
        metric_name="cpu_utilization_5s",
        label="CPU utilization (5s avg)",
        render_func=lambda v: f"{v:.0f}%",
        boundaries=(0.0, 100.0),
    )

    # Additional metrics for other averages (informational, no alerting)
    yield Metric("cpu_utilization_1s", cpu_1s, boundaries=(0, 100))
    yield Metric("cpu_utilization_60s", cpu_60s, boundaries=(0, 100))
    yield Metric("cpu_utilization_300s", cpu_300s, boundaries=(0, 100))

    # Details about all averages
    yield Result(
        state=State.OK,
        notice=f"1s: {cpu_1s}%, 60s: {cpu_60s}%, 300s: {cpu_300s}%",
    )


snmp_section_ruckus_cpu = SimpleSNMPSection(
    name="ruckus_cpu",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Ruckus Wireless, Inc. Stacking System"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1991.1.1.2.11.1.1.5.1.1",
        oids=["1", "5", "60", "300"],
    ),
    parse_function=parse_ruckus_cpu,
)


check_plugin_ruckus_cpu = CheckPlugin(
    name="ruckus_cpu",
    service_name="CPU Utilization",
    discovery_function=inventory_ruckus_cpu,
    check_function=check_ruckus_cpu,
    check_default_parameters={
        "cpu_levels_upper": ("fixed", (80.0, 90.0)),
        # "cpu_levels_lower": ("fixed", (5.0, 2.0)),  # optional
    },
    check_ruleset_name="ruckus_cpu",
)
