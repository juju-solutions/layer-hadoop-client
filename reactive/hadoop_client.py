# pylint: disable=unused-argument
from charms.reactive import when, when_not, when_not_all, is_state
from charmhelpers.core import hookenv
from charms import layer


if hookenv.metadata()['name'] == 'hadoop-client':
    # only report Ready status if deployed as standalone client,
    # not if used as a base layer
    @when('hadoop.installed')
    def report_ready(hadoop):
        hookenv.status_set('active', 'ready')


@when_not_all('hadoop.joined', 'java.ready')
def report_blocked():
    cfg = layer.options('hadoop-client')
    if not cfg.get('silent'):
        missing = []
        if not is_state('hadoop.joined'):
            missing.append('relation to hadoop plugin')
        if not is_state('java.ready'):
            missing.append('java')
        missing = ' & '.join(missing)
        hookenv.status_set('blocked', 'waiting for {}'.format(missing))


@when('hadoop.joined', 'java.ready')
def proxy_java(hadoop, java):
    hadoop.set_java_info(java.java_home(), java.java_version())


@when('hadoop.joined')
@when_not('hadoop.installed')
def report_waiting(hadoop):
    cfg = layer.options('hadoop-client')
    if not cfg.get('silent'):
        hookenv.status_set('waiting', 'waiting for plugin to become ready')
