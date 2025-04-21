# scripts/debug_bootstrap_setup.py

from fhe_ai_inference.params_bootstrap import build_bootstrappable_context

context = build_bootstrappable_context()
print("Context generated")

try:
    context.EvalBootstrapSetup()
    print("✅ EvalBootstrapSetup completed successfully")
except Exception as e:
    print("❌ EvalBootstrapSetup failed:", e)
