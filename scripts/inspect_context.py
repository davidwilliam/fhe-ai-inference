# scripts/inspect_context.py

from fhe_ai_inference.params import FHEContextBuilder


def display_context_info(depth, scale, ring_dim=None):
    context = FHEContextBuilder.build(depth, scale, ring_dim)
    print(
        f"--- Context with Depth={depth}, "
        f"ScaleMod={scale}, "
        f"RingDim={ring_dim or 'default'} ---"
    )
    print("Ring Dimension     :", context.GetRingDimension())
    print("Scaling Modulus    :", scale)
    print("Multiplicative Depth (configured):", depth)
    print()


if __name__ == "__main__":
    display_context_info(2, 50)
    display_context_info(4, 55)
    display_context_info(4, 50, ring_dim=32768)
