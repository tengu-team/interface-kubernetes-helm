import os
from charms.reactive import (
    when,
    when_not,
    set_flag,
    clear_flag,
    Endpoint,
)


class KubernetesHelmRequires(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def helm_joined(self):
        set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def helm_broken(self):
        clear_flag(self.expand_name('available'))

    @when('endpoint.{endpoint_name}.changed.charts_status')
    def changed_status(self):
        set_flag(self.expand_name('status'))
        clear_flag(self.expand_name('changed.charts_status'))

    def send_charts_request(self, charts):
        """
        Args:
        charts (list): list where each element is a dict containing
                       the following fields:
                       [{
                           'name': 'chart_name',
                           'repo': 'http://10.10.138.60:1323/charts/'
                       }]

        IMPORTANT: the names have to be unique
        """
        for relation in self.relations:
            relation.to_publish['chart_requests'] = charts
            relation.to_publish['uuid'] = self.get_uuid()

    def get_status(self):
        status = None
        for relation in self.relations:
            for unit in relation.units:
                if unit.received['charts_status']:
                    status = unit.received['charts_status']
        return status

    def get_uuid(self):
        unit_name = os.environ['JUJU_UNIT_NAME']
        model_uuid = os.environ['JUJU_MODEL_UUID']
        return model_uuid + '_' + unit_name
