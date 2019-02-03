# Test ConfigMapHash and SecretHash equivalents
# tests based on https://github.com/kubernetes/kubernetes/pull/49961

from openshift.dynamic.apply import merge

tests = [
    dict(
        last_applied = dict(
            kind="ConfigMap",
            metadata=dict(name="cm_no_change"),
            data=dict(one="1", two="2")
        ),
        desired = dict(
            kind="ConfigMap",
            metadata=dict(name="cm_no_change"),
            data=dict(one="1", two="2")
        ),
        expected = {}
    ),
    dict(
        last_applied = dict(
            kind="ConfigMap",
            metadata=dict(name="cm_add_one"),
            data=dict(one="1", two="2")
        ),
        desired = dict(
            kind="ConfigMap",
            metadata=dict(name="cm_add_one"),
            data=dict(one="1", two="2", three="3")
        ),
        expected = dict(data=dict(three="3"))
    ),
    dict(
        last_applied = dict(
            kind="ConfigMap",
            metadata=dict(name="cm_replace_one"),
            data=dict(one="1", two="2")
        ),
        desired = dict(
            kind="ConfigMap",
            metadata=dict(name="cm_replace_one"),
            data=dict(one="1", three="3")
        ),
        expected = dict(data=dict(two=None, three="3"))
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="svc_no_change"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="svc_no_change"),
            spec=dict(ports=[dict(port=8080, protocol='TCP', name="http")])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="svc_no_change"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        expected = {}
    ),
    dict(
        last_applied = dict(
            kind="Service",
            metadata=dict(name="svc_change_port"),
            spec=dict(ports=[dict(port=8080, name="http")])
        ),
        actual = dict(
            kind="Service",
            metadata=dict(name="svc_change_port"),
            spec=dict(ports=[dict(port=8080, protocol='TCP', name="http")])
        ),
        desired = dict(
            kind="Service",
            metadata=dict(name="svc_change_port"),
            spec=dict(ports=[dict(port=8081, name="http")])
        ),
        expected = dict(spec=dict(ports=[dict(port=8081, name="http")]))
    ),
    dict(
        last_applied = {},
        desired = dict(
            kind="Namespace",
            metadata=dict(name="ns_new")
        ),
        expected = dict(
            kind="Namespace",
            metadata=dict(name="ns_new")
        ),
    ),
    dict(
        last_applied = dict(
            kind="Namespace",
            metadata=dict(name="ns_no_change")
        ),
        desired = dict(
            kind="Namespace",
            metadata=dict(name="ns_no_change")
        ),
        expected = {}
    )
]


def test_merges():
    for test in tests:
        assert(merge(test['last_applied'], test['desired'], test.get('actual', test['last_applied'])) == test['expected'])
