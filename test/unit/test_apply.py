from openshift.dynamic.apply import merge

tests = [

    dict(
        last_applied = dict(
            kind="ConfigMap",
            metadata=dict(name="foo"),
            data=dict(one="1", two="2")
        ),
        desired = dict(
            kind="ConfigMap",
            metadata=dict(name="foo"),
            data=dict(one="1", two="2")
        ),
        expected = {}
    ),
    dict(
        last_applied = dict(
            kind="ConfigMap",
            metadata=dict(name="foo"),
            data=dict(one="1", two="2")
        ),
        desired = dict(
            kind="ConfigMap",
            metadata=dict(name="foo"),
            data=dict(one="1", two="2", three="3")
        ),
        expected = dict(data=dict(three="3"))
    ),
    dict(
        last_applied = dict(
            kind="ConfigMap",
            metadata=dict(name="foo"),
            data=dict(one="1", two="2")
        ),
        desired = dict(
            kind="ConfigMap",
            metadata=dict(name="foo"),
            data=dict(one="1", three="3")
        ),
        expected = dict(data=dict(two=None, three="3"))
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, protocol='TCP', name="http")])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        expected = dict(spec=dict(ports=[dict(port=8080, protocol='TCP', name="http")]))
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, protocol='TCP', name="http")])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8081, name="http")])
        ),
        expected = dict(spec=dict(ports=[dict(port=8081, name="http")]))
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, protocol='TCP', name="http")])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8443, name="https"), dict(port=8080, name="http")])
        ),
        expected = dict(spec=dict(ports=[dict(port=8443, name="https"), dict(port=8080, name="http", protocol='TCP')]))
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8443, name="https"), dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8443, protocol='TCP', name="https"), dict(port=8080, protocol='TCP', name='http')])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        expected = dict(spec=dict(ports=[dict(port=8080, name="http", protocol='TCP')]))
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8443, name="https", madeup="xyz"), dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8443, protocol='TCP', name="https", madeup="xyz"), dict(port=8080, protocol='TCP', name='http')])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="foo"),
            spec=dict(ports=[dict(port=8443, name="https")])
        ),
        expected = dict(spec=dict(ports=[dict(port=8443, name="https", protocol='TCP')]))
    ),

    # This next one is based on a real world case where definition was mostly
    # str type and everything else was mostly unicode type (don't ask me how)
    dict(
        last_applied = {
            u'kind': u'ConfigMap',
            u'data': {u'one': '1', 'three': '3', 'two': '2'},
            u'apiVersion': u'v1',
            u'metadata': {u'namespace': u'apply', u'name': u'apply-configmap'}
        },
        actual = {
            u'kind': u'ConfigMap',
            u'data': {u'one': '1', 'three': '3', 'two': '2'},
            u'apiVersion': u'v1',
            u'metadata': {u'namespace': u'apply', u'name': u'apply-configmap',
                          u'resourceVersion': '1714994',
                          u'creationTimestamp': u'2019-08-17T05:08:05Z', u'annotations': {},
                          u'selfLink': u'/api/v1/namespaces/apply/configmaps/apply-configmap',
                          u'uid': u'fed45fb0-c0ac-11e9-9d95-025000000001'}
        },
        desired = {
            'kind': u'ConfigMap',
            'data': {'one': '1', 'three': '3', 'two': '2'},
            'apiVersion': 'v1',
            'metadata': {'namespace': 'apply', 'name': 'apply-configmap'}
        },
        expected = dict()
    ),
    # apply a Deployment, then scale the Deployment (which doesn't affect last-applied)
    # then apply the Deployment again. Should un-scale the Deployment
    dict(
        last_applied = {
            'kind': u'Deployment',
            'spec': {
                'replicas': 1,
                'template': {
                    'spec': {
                        'containers': [
                            {
                                'name': 'this_must_exist',
                                'envFrom': [
                                    {
                                        'configMapRef': {
                                            'name': 'config-xyz'
                                        }
                                    },
                                    {
                                        'secretRef': {
                                            'name': 'config-wxy'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            'metadata': {
                'namespace': 'apply',
                'name': u'apply-deployment'
            }
        },
        actual = {
            'kind': u'Deployment',
            'spec': {
                'replicas': 0,
                'template': {
                    'spec': {
                        'containers': [
                            {
                                'name': 'this_must_exist',
                                'envFrom': [
                                    {
                                        'configMapRef': {
                                            'name': 'config-xyz'
                                        }
                                    },
                                    {
                                        'secretRef': {
                                            'name': 'config-wxy'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            'metadata': {
                'namespace': 'apply',
                'name': u'apply-deployment'
            }
        },
        desired = {
            'kind': u'Deployment',
            'spec': {
                'replicas': 1,
                'template': {
                    'spec': {
                        'containers': [
                            {
                                'name': 'this_must_exist',
                                'envFrom': [
                                    {
                                        'configMapRef': {
                                            'name': 'config-abc'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            'metadata': {
                'namespace': 'apply',
                'name': u'apply-deployment'
            }
        },
        expected = {
            'spec' : {
                'replicas': 1,
                'template': {
                    'spec': {
                        'containers': [
                            {
                                'name': 'this_must_exist',
                                'envFrom': [
                                    {
                                        'configMapRef': {
                                            'name': 'config-abc'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    )
]


def test_merges():
    for test in tests:
        assert(merge(test['last_applied'], test['desired'], test.get('actual', test['last_applied'])) == test['expected'])
