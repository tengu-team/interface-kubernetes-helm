from charms.reactive import (
    when,
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

    @when('endpoint.{endpoint_name}.changed.chart_requests')
    def changed(self):
        set_flag(self.expand_name('new-chart-requests'))

    def get_chart_requests(self):
        """
        Return all juju_app :
        {
            'model_uuid_unit_name': {
                'charts': [{
                    'name': 'chart_name',
                    'repo': 'http://10.10.138.60:1323/charts/'
                }],
            }
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
                chart_requests[uuid] ={
                    'charts': requests
                } 
        return chart_requests

    def send_status(self, status):
        """
        Return chart deployment status.
        """
        # TODO TEST IF ONE TO ONE COMMUNICATION WORKS
        for relation in self.relations:
            unit = relation.unit[0]
            uuid = unit.received['uuid']
            relation.to_publish['charts_status'] = status[uuid]