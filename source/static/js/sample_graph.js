const sample_graph={
  "nodes": {
    "0": {
      "id": 0,
      "label": "driver",
      "data": {
        "tags": {
          "client-uuid": "6650699757845d5",
          "hostname": "2105776318cd",
          "ip": "172.17.0.3",
          "jaeger.version": "Go-2.23.1",
          "serviceName": "driver"
        }
      }
    },
    "1": {
      "id": 1,
      "label": "customer",
      "data": {
        "tags": {
          "client-uuid": "10d085ac339ff1e3",
          "hostname": "2105776318cd",
          "ip": "172.17.0.3",
          "jaeger.version": "Go-2.23.1",
          "serviceName": "customer"
        }
      }
    },
    "2": {
      "id": 2,
      "label": "route",
      "data": {
        "tags": {
          "client-uuid": "2cb0597100495c98",
          "hostname": "2105776318cd",
          "ip": "172.17.0.3",
          "jaeger.version": "Go-2.23.1",
          "serviceName": "route"
        }
      }
    },
    "3": {
      "id": 3,
      "label": "frontend",
      "data": {
        "tags": {
          "client-uuid": "300306bbe7dd0d07",
          "hostname": "2105776318cd",
          "ip": "172.17.0.3",
          "jaeger.version": "Go-2.23.1",
          "serviceName": "frontend"
        }
      }
    },
    "4": {
      "id": 4,
      "label": "redis",
      "data": {
        "tags": {
          "client-uuid": "3e1881cd7f04c1f3",
          "hostname": "2105776318cd",
          "ip": "172.17.0.3",
          "jaeger.version": "Go-2.23.1",
          "serviceName": "redis"
        }
      }
    },
    "5": {
      "id": 5,
      "label": "mysql",
      "data": {
        "tags": {
          "client-uuid": "7e04c33a21c1453e",
          "hostname": "2105776318cd",
          "ip": "172.17.0.3",
          "jaeger.version": "Go-2.23.1",
          "serviceName": "mysql"
        }
      }
    }
  },
  "edges": {
    "0": {
      "id": 0,
      "label": "/driver.DriverService/FindNearest",
      "source": 0,
      "target": 4,
      "data": {
        "duration": 174788,
        "logs": {
          "1606579665241076": {
            "event": "Searching for nearby drivers",
            "level": "info",
            "location": "211,653"
          },
          "1606579665309666": {
            "event": "Retrying GetDriver after error",
            "error": "redis timeout",
            "level": "error",
            "retry_no": 1
          },
          "1606579665373579": {
            "event": "Retrying GetDriver after error",
            "error": "redis timeout",
            "level": "error",
            "retry_no": 1
          },
          "1606579665415608": {
            "event": "Search successful",
            "level": "info",
            "num_drivers": 10
          }
        },
        "tags": {
          "component": "gRPC",
          "span.kind": "server",
          "internal.span.format": "proto"
        }
      }
    },
    "1": {
      "id": 1,
      "label": "HTTP GET /customer",
      "source": 1,
      "target": 5,
      "data": {
        "duration": 291891,
        "logs": {
          "1606579664948073": {
            "event": "HTTP request received",
            "level": "info",
            "method": "GET",
            "url": "/customer?customer=567"
          },
          "1606579664948310": {
            "event": "Loading customer",
            "customer_id": "567",
            "level": "info"
          }
        },
        "tags": {
          "span.kind": "server",
          "http.method": "GET",
          "http.url": "/customer?customer=567",
          "component": "net/http",
          "http.status_code": 200,
          "internal.span.format": "proto"
        }
      }
    },
    "2": {
      "id": 2,
      "label": "HTTP GET /route",
      "source": 2,
      "target": 2,
      "data": {
        "duration": 52705,
        "logs": {
          "1606579665539197": {
            "event": "HTTP request received",
            "level": "info",
            "method": "GET",
            "url": "/route?dropoff=211%2C653&pickup=689%2C934"
          }
        },
        "tags": {
          "span.kind": "server",
          "http.method": "GET",
          "http.url": "/route?dropoff=211%2C653&pickup=689%2C934",
          "component": "net/http",
          "http.status_code": 200,
          "internal.span.format": "proto"
        }
      }
    },
    "3": {
      "id": 3,
      "label": "HTTP GET /dispatch",
      "source": 3,
      "target": 3,
      "data": {
        "duration": 662126,
        "logs": {
          "1606579664947777": {
            "event": "HTTP request received",
            "level": "info",
            "method": "GET",
            "url": "/dispatch?customer=567&nonse=0.9479018769558671"
          },
          "1606579664947842": {
            "event": "Getting customer",
            "customer_id": "567",
            "level": "info"
          },
          "1606579665240288": {
            "event": "Found customer",
            "level": "info"
          },
          "1606579665240368": {
            "event": "baggage",
            "key": "customer",
            "value": "Amazing Coffee Roasters"
          },
          "1606579665240373": {
            "event": "Finding nearest drivers",
            "level": "info",
            "location": "211,653"
          },
          "1606579665416269": {
            "event": "Found drivers",
            "level": "info"
          },
          "1606579665416426": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "813,734"
          },
          "1606579665416548": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "122,838"
          },
          "1606579665416888": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "10,738"
          },
          "1606579665440575": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "361,440"
          },
          "1606579665462991": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "845,109"
          },
          "1606579665471924": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "207,801"
          },
          "1606579665519211": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "648,416"
          },
          "1606579665520213": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "779,604"
          },
          "1606579665538600": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "689,934"
          },
          "1606579665559067": {
            "event": "Finding route",
            "dropoff": "211,653",
            "level": "info",
            "pickup": "346,342"
          },
          "1606579665609475": {
            "event": "Found routes",
            "level": "info"
          },
          "1606579665609590": {
            "event": "Dispatch successful",
            "driver": "T765730C",
            "eta": "2m0s",
            "level": "info"
          }
        },
        "tags": {
          "sampler.type": "const",
          "sampler.param": true,
          "span.kind": "server",
          "http.method": "GET",
          "http.url": "/dispatch?customer=567&nonse=0.9479018769558671",
          "component": "net/http",
          "http.status_code": 200,
          "internal.span.format": "proto"
        }
      }
    },
    "4": {
      "id": 4,
      "label": "HTTP GET",
      "source": 3,
      "target": 1,
      "data": {
        "duration": 50142,
        "logs": {
          "1606579665559338": {
            "event": "GetConn"
          },
          "1606579665559343": {
            "event": "GotConn"
          },
          "1606579665559384": {
            "event": "WroteHeaders"
          },
          "1606579665559386": {
            "event": "WroteRequest"
          },
          "1606579665609359": {
            "event": "GotFirstResponseByte"
          },
          "1606579665609395": {
            "event": "PutIdleConn"
          },
          "1606579665609459": {
            "event": "ClosedBody"
          }
        },
        "tags": {
          "span.kind": "client",
          "component": "net/http",
          "http.method": "GET",
          "http.url": "0.0.0.0:8083",
          "net/http.reused": true,
          "net/http.was_idle": true,
          "http.status_code": 200,
          "internal.span.format": "proto"
        }
      }
    },
    "5": {
      "id": 5,
      "label": "HTTP GET",
      "source": 3,
      "target": 2,
      "data": {
        "duration": 50142,
        "logs": {
          "1606579665559338": {
            "event": "GetConn"
          },
          "1606579665559343": {
            "event": "GotConn"
          },
          "1606579665559384": {
            "event": "WroteHeaders"
          },
          "1606579665559386": {
            "event": "WroteRequest"
          },
          "1606579665609359": {
            "event": "GotFirstResponseByte"
          },
          "1606579665609395": {
            "event": "PutIdleConn"
          },
          "1606579665609459": {
            "event": "ClosedBody"
          }
        },
        "tags": {
          "span.kind": "client",
          "component": "net/http",
          "http.method": "GET",
          "http.url": "0.0.0.0:8083",
          "net/http.reused": true,
          "net/http.was_idle": true,
          "http.status_code": 200,
          "internal.span.format": "proto"
        }
      }
    },
    "6": {
      "id": 6,
      "label": "HTTP GET: /customer",
      "source": 3,
      "target": 3,
      "data": {
        "duration": 292389,
        "logs": {},
        "tags": {
          "internal.span.format": "proto"
        }
      }
    },
    "7": {
      "id": 7,
      "label": "/driver.DriverService/FindNearest",
      "source": 3,
      "target": 0,
      "data": {
        "duration": 175836,
        "logs": {},
        "tags": {
          "span.kind": "client",
          "component": "gRPC",
          "internal.span.format": "proto"
        }
      }
    },
    "8": {
      "id": 8,
      "label": "HTTP GET: /route",
      "source": 3,
      "target": 3,
      "data": {
        "duration": 50151,
        "logs": {},
        "tags": {
          "internal.span.format": "proto"
        }
      }
    },
    "9": {
      "id": 9,
      "label": "FindDriverIDs",
      "source": 4,
      "target": 4,
      "data": {
        "duration": 18621,
        "logs": {
          "1606579665259724": {
            "event": "Found drivers",
            "level": "info"
          }
        },
        "tags": {
          "param.location": "211,653",
          "span.kind": "client",
          "internal.span.format": "proto"
        }
      }
    },
    "10": {
      "id": 10,
      "label": "GetDriver",
      "source": 4,
      "target": 4,
      "data": {
        "duration": 11423,
        "logs": {},
        "tags": {
          "param.driverID": "T752227C",
          "span.kind": "client",
          "internal.span.format": "proto"
        }
      }
    },
    "11": {
      "id": 11,
      "label": "SQL SELECT",
      "source": 5,
      "target": 5,
      "data": {
        "duration": 291349,
        "logs": {
          "1606579664948547": {
            "event": "Acquired lock with 0 transactions waiting behind"
          }
        },
        "tags": {
          "span.kind": "client",
          "peer.service": "mysql",
          "sql.query": "SELECT * FROM customer WHERE customer_id=567",
          "request": "6708-4",
          "internal.span.format": "proto"
        }
      }
    }
  }
};