from charms.reactive import (
    when,
    when_any,
    when_not,
    set_flag,
    clear_flag,
    Endpoint,
)


class KubernetesHelmProvides(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def helm_joined(self):
        if any(unit.received['chart_requests'] for unit in self.all_units):
            set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def helm_broken(self):
        clear_flag(self.expand_name('available'))

    # Remove departed flag when issue 
    # https://github.com/juju-solutions/charms.reactive/issues/170
    # is resolved
    @when_any('endpoint.{endpoint_name}.changed.chart_requests',
              'endpoint.{endpoint_name}.departed')
    def changed(self):
        set_flag(self.expand_name('new-chart-requests'))
        clear_flag(self.expand_name('changed.chart_requests'))
        clear_flag(self.expand_name('departed'))



    @when('endpoint.{endpoint_name}.changed.status_update_request')
    def status_update_request(self):
        clear_flag(self.expand_name('changed.status_update_request'))
        if self.get_status_update_subscribers():
            set_flag(self.expand_name('status-update'))
        else:
            clear_flag(self.expand_name('status-update'))

    def get_chart_requests(self):
        """
        Return all chart requests in the following format:
        {
            'model_uuid_unit_name':[{
                    'name': 'chart_name',
                    'repo': 'http://10.10.138.60:1323/charts/'
                }],
        }
        """
        chart_requests = {}
        for relation in self.relations:
            requests = []
            for unit in relation.units:
                if unit.received['chart_requests']:
                    requests.extend(unit.received['chart_requests'])
            if requests:
                uuid = unit.received['uuid']
                chart_requests[uuid] = requests
        return chart_requests

    def send_status(self, status):
        """
        Send chart deployment status.
        """
        for relation in self.relations:
            unit = relation.units[0]
            uuid = unit.received['uuid']
            if uuid in status:
                relation.to_publish['charts_status'] = status[uuid]

    def get_status_update_subscribers(self):
        units = {}
        for relation in self.relations:            
            for unit in relation.units:
                if unit.received['status_update_request'] == "sub":
                    units[unit.received['uuid']] = ""
        return units.keys()
