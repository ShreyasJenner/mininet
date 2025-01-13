import requests
from requests.auth import HTTPBasicAuth

# Controller parameters
controller_ip = "192.168.56.102"
username = "admin"
password = "admin"

# Function to add a flow entry to a switch
def add_flow_to_switch(switch_id, input_port, output_port, host_ip, flow_id):
    url = f"http://{controller_ip}:8181/restconf/config/opendaylight-inventory:nodes/node/{switch_id}/table/0/flow/{flow_id}"

    flow_entry = {
        "flow": [
            {
                "id": str(flow_id),
                "priority": 100,
                "match": {
                    "in-port": input_port,
                    "ethernet-match": {
                        "ethernet-type": {
                            # Match IPv4 packets
                            "type": "0x0800"
                        }
                    },
                    "ipv4-destination": f"{host_ip}/32"
                },
                "instructions": {
                    "instruction": [
                        {
                            "order": 0,
                            "apply-actions": {
                                "action": [
                                    {
                                        "order": 0,
                                        "output-action": {
                                            "output-node-connector": output_port
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                },
                "table_id": "0"
            }
        ]
    }

    try:
        res = requests.put(url, json=flow_entry, auth=HTTPBasicAuth(username, password))

        if res.status_code in [200, 201]:
            print(f"Flow entry added to {switch_id}")
        else:
            print(f"Failed to add flow entry to {switch_id}. Status code: {res.status_code}")
            print("Response:", res.text)
    except Exception as e:
        print(f"Error occurred while adding flow to {switch_id}: {e}")

if __name__ == "__main__":
    # Switch IDs
    switch_id_1 = "openflow:1"
    switch_id_2 = "openflow:2"
    switch_id_3 = "openflow:3"

    # Add flows for s1
    add_flow_to_switch(switch_id_1, "1", "2", "10.0.0.3", "1")  # h1 -> s2 for h3
    add_flow_to_switch(switch_id_1, "2", "1", "10.0.0.1", "1")  # h3 -> s1 for h1

    # Add flows for s2
    add_flow_to_switch(switch_id_2, "2", "3", "10.0.0.3", "1")  # s1 -> s3 for h3
    add_flow_to_switch(switch_id_2, "3", "2", "10.0.0.1", "1")  # s3 -> s1 for h1

    # Add flows for s3
    add_flow_to_switch(switch_id_3, "1", "2", "10.0.0.3", "1")  # s2 -> h3
    add_flow_to_switch(switch_id_3, "2", "1", "10.0.0.1", "1")  # h3 -> s2
