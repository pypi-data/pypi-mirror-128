def generate_config(api_addr: str = "::1", api_port: int = 1118) -> str:
    """ Generate basic V2ray configuration file with gRPC api enabled"""
    return """{
  "inbounds": [{
      "port": %(port)d,
      "listen": "%(addr)s",
      "protocol": "dokodemo-door",
      "settings": {
        "address": "127.0.0.1"
      },
      "tag": "api"
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {},
      "tag": "direct"
    }
  ],
  "policy": {
    "levels": {
      "0": {
        "statsUserUplink": true,
        "statsUserDownlink": true
      }
    },
    "system": {
      "statsInboundUplink": true,
      "statsInboundDownlink": true
    }
  },
  "stats": {},
  "api": {
    "tag": "api",
    "services": [
      "HandlerService",
      "StatsService"
    ]
  },
  "routing": {
    "settings": {
      "rules": [
        {
          "inboundTag": [
            "api"
          ],
          "outboundTag": "api",
          "type": "field"
        }
      ]
    },
    "strategy": "rules"
  }
}
""" % {
        "port": api_port,
        "addr": api_addr
    }
