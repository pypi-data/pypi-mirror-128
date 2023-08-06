from __future__ import annotations
import logging
from datetime import datetime
from dataclasses import dataclass

from pyaware import events

log = logging.getLogger(__file__)


@events.enable
@dataclass
class Topology:
    device_id: str = ""
    serial_number: str = ""
    include_serial: bool = False
    network: dict = None

    def __post_init__(self):
        self.topologies = {}
        self.identify()
        if self.include_serial:
            self.topic_types = {
                "topology": "topology_serial",
            }
        else:
            self.topic_types = {
                "topology": "topology",
            }
        events.publish("request_topology")

    @events.subscribe(topic="update_gateway_network/#")
    def update_network(self, data):
        self.network = data
        events.publish("request_topology")

    def identify(self):
        data = {}
        if self.network:
            data["network"] = self.network
        return {
            "values": data,
            "timestamp": datetime.utcnow(),
            "children": list(self.topologies.values()),
        }

    @events.subscribe(topic="request_topology")
    def update_topology(self):
        """
        Updates the topology for a given device and resends all the currently connected devices
        :param data: Device topology payload derived from identify method
        :param timestamp: Timestamp of the topology
        :param topic: device_topology/{device_id}
        :return:
        """
        payload = self.identify()
        log.info(f"New topology:  {payload}")
        events.publish(
            f"trigger_send",
            data=payload,
            timestamp=datetime.utcnow(),
            topic_type=self.topic_types["topology"],
            device_id=self.device_id,
            serial_number=self.serial_number,
        )

    @events.subscribe(topic="device_topology/#", parse_topic=True)
    def build_topology(self, data, timestamp, topic):
        """
        Updates the topology for a given device and resends all the currently connected devices
        :param data: Device topology payload derived from identify method
        :param timestamp: Timestamp of the topology
        :param topic: device_topology/{device_id}
        :return:
        """
        device_id = topic.split("/")[-1]
        self.topologies[device_id] = data
        self.update_topology()
