# Test ConfigMap and Secret marshalling
# tests based on https://github.com/kubernetes/kubernetes/pull/49961

from openshift.helper.hashes import marshal

tests = [
    dict(
        resource=dict(
            kind="ConfigMap",
            name="",
            data=dict(),
        ),
        expected='{"data":{},"kind":"ConfigMap","name":""}'
    ),
    dict(
        resource=dict(
            kind="ConfigMap",
            name="",
            data=dict(
                one=""
            ),
        ),
        expected='{"data":{"one":""},"kind":"ConfigMap","name":""}'
    ),
    dict(
        resource=dict(
            kind="ConfigMap",
            name="",
            data=dict(
                two="2",
                one="",
                three="3",
            ),
        ),
        expected='{"data":{"one":"","three":"3","two":"2"},"kind":"ConfigMap","name":""}'
    ),
    dict(
        resource=dict(
            kind="Secret",
            type="my-type",
            name="",
            data=dict(),
        ),
        expected='{"data":{},"kind":"Secret","name":"","type":"my-type"}'
    ),
    dict(
        resource=dict(
            kind="Secret",
            type="my-type",
            name="",
            data=dict(
                one=""
            ),
        ),
        expected='{"data":{"one":""},"kind":"Secret","name":"","type":"my-type"}'
    ),
    dict(
        resource=dict(
            kind="Secret",
            type="my-type",
            name="",
            data=dict(
                two="Mg==",
                one="",
                three="Mw==",
            ),
        ),
        expected='{"data":{"one":"","three":"Mw==","two":"Mg=="},"kind":"Secret","name":"","type":"my-type"}'
    ),
]

def test_marshal():
    for test in tests:
        assert(marshal(test['resource'], sorted(test['resource'].keys())) == test['expected'])
