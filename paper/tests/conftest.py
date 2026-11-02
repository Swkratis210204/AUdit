"""Settings shared by the tests of the paper code: the repository root is put on the path so that ``paper`` can be imported."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "polalign" / "src"))
try:
    import matplotlib

    matplotlib.use("Agg")
except ImportError:
    pass
