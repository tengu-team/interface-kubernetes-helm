# Overview
This interface is used for charms who want to install Helm charts on a Kubernetes cluster.
## Usage
### Requires
By requiring the `kubernetes-helm` interface, your charm wants to install Helm charts by sending installation requests.

***states***
- `endpoint.{relation-name}.available` set when a Helm provider has joined the relation.
- `endpoint.{relation-name}.status` set when a status update is received.

***methods***
- `send_charts_request(charts)` used to install charts. `charts` is expected to have the following format.
```
[
    {
         'name': 'chart-name',
         'repo': 'http://10.10.138.60:1323/charts/'
    }, ...
]
```
- `get_status()` Should be called after the `endpoint.{relation-name}.status` flag is set. Returns a status update on the requested charts.
- `get_uuid()` Used internally to attach a human readable uuid to the request.

### Provides
By providing the `kubernetes-helm` interface, your charm installs Helm charts.

***states***
- `endpoint.{relation-name}.available` set when a Helm requirer has joined the relation and a chart installation request has been sent.
- `endpoint.{relation-name}.new-chart-requests` is set when a change has been detected in requested charts.

***methods***

- `get_chart_requests()` returns all chart requests in the following format.
```
{
    'uuid': [{
        'name': 'chart-name',
        'repo': 'http://10.10.138.60:1323/charts/'
    }, ...]
    , ...
}
```
- `send_status()` Send a status update on the installed charts.

## Authors
This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab/en) of [Ghent University](https://www.ugent.be/en) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.
- Sander Borny <sander.borny@ugent.be>
