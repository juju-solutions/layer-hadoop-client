# pylint: disable=unused-argument
from charms.reactive import when, when_not
from charmhelpers.core import hookenv


if hookenv.metadata()['name'] == 'hadoop-client':
    # only report status if deployed as standalone client,
    # not if used as a base layer
    @when('hadoop.installed')
    def report_ready(hadoop):
        hookenv.status_set('active', 'ready')

    @when_not('hadoop.joined')
    def report_blocked():
        hookenv.status_set('blocked', 'waiting for relation to hadoop plugin')

    @when('hadoop.joined')
    @when_not('hadoop.installed')
    def report_waiting_for_hadoop(hadoop):
        hookenv.status_set('waiting', 'waiting for plugin to become ready')

    @when('java.connected')
    @when_not('java.ready')
    def report_waiting_for_java(hadoop):
        hookenv.status_set('waiting', 'waiting for java to become ready')


@when('hadoop.joined', 'java.ready')
def proxy_java(hadoop, java):
    hadoop.set_java_info(java.java_home(), java.java_version())
