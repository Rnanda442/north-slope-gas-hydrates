from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd


MODULE_PATH = Path(__file__).resolve().parents[1] / "01_pipeline" / "generate_doe_equation_derived_visuals.py"
SPEC = importlib.util.spec_from_file_location("generate_doe_equation_derived_visuals", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def test_equation_visual_generator_outputs_pngs_and_readiness(tmp_path: Path) -> None:
    rng = np.random.default_rng(42)
    rows = 120
    input_csv = tmp_path / "private_like_input.csv"
    pd.DataFrame(
        {
            "WELL": rng.choice(["MTE", "IGS"], size=rows),
            "DEPTH": rng.uniform(350, 1200, size=rows),
            "RHOB": rng.normal(2.18, 0.06, size=rows),
            "Rt": np.exp(rng.normal(np.log(20), 0.5, size=rows)),
            "VP": rng.normal(3.05, 0.25, size=rows),
            "VS": rng.normal(1.45, 0.16, size=rows),
            "temperature_c": rng.normal(6, 2, size=rows),
        }
    ).to_csv(input_csv, index=False)

    outputs = module.run(input_csv, tmp_path / "outputs", module.Constants())

    for path in outputs.values():
        assert path.exists()
        assert path.stat().st_size > 0

    readiness = pd.read_csv(outputs["readiness_csv"])
    assert {"rho_b", "Rt", "Sh", "mu-rho", "lambda-rho"}.issubset(set(readiness["symbol"]))
    assert readiness.loc[readiness["symbol"].eq("Sh"), "status"].iloc[0] == "usable"
