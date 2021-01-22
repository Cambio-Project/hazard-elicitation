## MiSim

```
# MiSim architecture model

# Structure of a dependency
Dependency:
    - service: str
    - operation: str
    - probability: float

# Structure of an operation
Operation:
    - name: str
    - demand: int
    - dependencies: [Dependency]
    - circuitBreaker
        - rollingWindow: int
        - requestVolumeThreshold: int
        - errorThresholdPercentage: float
        - timeout: int
        - sleepWindow: int

# Structure of a service
Service:
    - name: str
    - instances: int
    - capacity: int
    - operations: [Operation]
    - patterns: [?]

# Top level property of the MiSim architecture model
- microservices : [Service]
```

```
# MiSim experiment model

# Structure of a generator
Generator:
    - microservice: str
    - operation: str
    - interval: float

# Structure of a chaosmonkey
Chaosmonkey:
    - microservice: str
    - instances: int
    - time: int

# Top level properties of the MiSim experiment model
- simulation_meta_data
    - experiment_name: str
    - model_name: str
    - duration: int
    - report: str
    - datapoints: int
    - seed: int
- request_generators: [Generator]
- chaosmonkeys: [Chaosmonkey]
```

## Jaeger

```
# Structure of a tag
Tag:
    - key: str
    - type: str
    - value: str

# Structure of a log
Log:
    - timestamp: int
    - field: [Tag]

# Structure of a reference type
ReferenceType:
    - refType: str
    - traceID: str
    - spanID: str

# Structure of a reference
Reference: [ReferenceType]

# Structure of a span
Span:
    - traceID: str
    - spanID: str
    - flags: int8
    - operationName: str
    - references: [Reference]
    - startTime: int
    - duration: int
    - tags: [Tag]
    - logs: [Log]
    - processID: p#
    - warnings: {}

# Structure of a process
Process:
    - serviceName: str
    - tags: [Tag]

# Structure of a trace
Trace:
    - traceID: str
    - spans: [Span]
    - processes: {p# : Process}
    - warnings: {}

# Top level properties of a Jaeger trace model
- data: [Trace]
- total: int
- limit: int
- offset: int
- errors: {}
```

## Zipkin

```
# Structure of an annotation
Annotation:
    - timestamp: int
    - value: str

# Structure of an endpoint
Endpoint:
    - serviceName: str
    - ipv4: str
    - port: int

# Structure of a trace
Trace:
    - traceId: str
    - id: str
    - kind: str
    - name: str
    - timestamp: int
    - duration: int
    - localEndpoint: Endpoint
    - remoteEndpoint: Endpoint
    - annotations: [Annotation]
    - tags: {str: str}

# Top level properties of a Zipkin trace model
[Trace]
```
