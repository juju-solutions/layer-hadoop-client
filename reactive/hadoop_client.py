# pylint: disable=unused-argument
from charms.reactive import when, when_not
from charmhelpers.core import hookenv


@when('hadoop.related', 'hadoop.installed')
def report_ready():
    hookenv.status_set('active', 'Ready')


@when_not('hadoop.related')
def report_blocked():
    hookenv.status_set('blocked', 'Waiting for relation to Hadoop Plugin')


@when('hadoop.related')
@when_not('hadoop.installed')
def report_waiting():
    hookenv.status_set('waiting', 'Waiting for Plugin to become ready')
