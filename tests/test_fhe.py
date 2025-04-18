# tests/test_fhe.py
import fhe_ai_inference.fhe as fhe_mod
from fhe_ai_inference.fhe import setup_ckks_context

def test_setup_ckks_context_default(monkeypatch):
    calls = {}

    def fake_genctx(scheme, poly_modulus_degree, security_level):
        calls['scheme'] = scheme
        calls['degree'] = poly_modulus_degree
        calls['level'] = security_level
        class FakeContext:
            def Enable(self, feat):
                calls['enabled'] = feat
        return FakeContext()

    # Patch or add GenCryptoContext on the module
    monkeypatch.setattr(fhe_mod, 'GenCryptoContext', fake_genctx, raising=False)

    # Invoke with defaults
    cc = setup_ckks_context()

    assert calls['scheme'] == 'CKKS'
    assert calls['degree'] == 8192
    assert calls['level'] == 128
    assert calls['enabled'] == 'PKCS'
    assert hasattr(cc, 'Enable')


def test_setup_ckks_context_custom(monkeypatch):
    calls = {}

    def fake_genctx(scheme, poly_modulus_degree, security_level):
        calls['scheme'] = scheme
        calls['degree'] = poly_modulus_degree
        calls['level'] = security_level
        class FakeContext:
            def Enable(self, feat):
                calls['enabled'] = feat
        return FakeContext()

    monkeypatch.setattr(fhe_mod, 'GenCryptoContext', fake_genctx, raising=False)

    custom_degree = 16384
    custom_level = 192
    cc = setup_ckks_context(
        poly_modulus_degree=custom_degree, security_level=custom_level
    )

    assert calls['scheme'] == 'CKKS'
    assert calls['degree'] == custom_degree
    assert calls['level'] == custom_level
    assert calls['enabled'] == 'PKCS'
    assert hasattr(cc, 'Enable')
