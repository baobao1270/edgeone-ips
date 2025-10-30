import os
from tencentcloud.common import credential
from tencentcloud.teo.v20220901 import teo_client, models
from dataclasses import dataclass
from typing import Callable, List, Literal, Optional, Sequence, Tuple, Union

SetNameType = Literal["current", "planned"]
AFIType = Literal["ipv4", "ipv6"]

@dataclass
class EdgeOnePullIP:
    set_name: SetNameType
    afi: AFIType
    address: str
    def __eq__(self, other):
        return isinstance(other, EdgeOnePullIP) and self.address == other.address
    def __hash__(self):
        return hash(self.address)

def request_ips(secret_id: str, secret_key: str, edgeone_zone_id: str) -> Tuple[Optional[models.CurrentOriginACL], Optional[models.NextOriginACL]]:
    cred = credential.Credential(secret_id, secret_key)
    client = teo_client.TeoClient(cred, "ap-guangzhou")
    req = models.DescribeOriginACLRequest()
    req.ZoneId = edgeone_zone_id
    res = client.DescribeOriginACL(req)
    return res.OriginACLInfo.CurrentOriginACL, res.OriginACLInfo.NextOriginACL

def handle_data(addr_list: List[EdgeOnePullIP], set_name: SetNameType, afi: AFIType, acl: Optional[Union[models.CurrentOriginACL, models.NextOriginACL]]):
    if acl is None:
        print(f"{set_name}.{afi} is empty, skipping")
        return
    addresses = {
        "ipv4": acl.EntireAddresses.IPv4,
        "ipv6": acl.EntireAddresses.IPv6,
    }[afi]
    for addr in addresses:
        addr_list.append(EdgeOnePullIP(set_name, afi, addr))

def build_release_file(addr_list: Sequence[EdgeOnePullIP], path: str, filter_func: Callable[[EdgeOnePullIP], bool]):
    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)
    lines = [x.address.strip() for x in set(filter(filter_func, addr_list))]
    lines = sorted(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved: {path} with {len(lines)} addresses.")

def main():
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    edgeone_zone_id =  os.environ.get("TENCENTCLOUD_EDGEONE_ZONE_ID")
    current_acl, planned_acl = request_ips(secret_id, secret_key, edgeone_zone_id)
    addr_list = []
    handle_data(addr_list, "current", "ipv4", current_acl)
    handle_data(addr_list, "current", "ipv6", current_acl)
    handle_data(addr_list, "planned", "ipv4", planned_acl)
    handle_data(addr_list, "planned", "ipv6", planned_acl)
    build_release_file(addr_list, "dist/current-ipv4",
                       lambda x: x.set_name == "current" and x.afi == "ipv4")
    build_release_file(addr_list, "dist/current-ipv6",
                       lambda x: x.set_name == "current" and x.afi == "ipv6")
    build_release_file(addr_list, "dist/current",
                       lambda x: x.set_name == "current")
    build_release_file(addr_list, "dist/planned-ipv4",
                       lambda x: x.set_name == "planned" and x.afi == "ipv4")
    build_release_file(addr_list, "dist/planned-ipv6",
                       lambda x: x.set_name == "planned" and x.afi == "ipv6")
    build_release_file(addr_list, "dist/planned",
                       lambda x: x.set_name == "planned")
    build_release_file(addr_list, "dist/edgeone-ipv4",
                       lambda x: x.afi == "ipv4")
    build_release_file(addr_list, "dist/edgeone-ipv6",
                       lambda x: x.afi == "ipv6")
    build_release_file(addr_list, "dist/edgeone",
                       lambda _: True)

if __name__ == '__main__':
    main()