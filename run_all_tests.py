from __future__ import annotations
import importlib.util
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
projects = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "test_main.py").exists())
suite = unittest.TestSuite()
errors = []
old_main = sys.modules.get("main")

for project in projects:
    # Load each standalone main.py under a unique name while exposing it temporarily as `main`
    # so each project's existing test_main.py remains unchanged and can be run in one process.
    module_name = "quantix_tool_" + project.name.replace("-", "_")
    main_spec = importlib.util.spec_from_file_location(module_name, project / "main.py")
    if main_spec is None or main_spec.loader is None:
        errors.append(f"Cannot load main.py for {project.name}")
        continue
    module = importlib.util.module_from_spec(main_spec)
    sys.modules[module_name] = module
    sys.modules["main"] = module
    sys.path.insert(0, str(project))
    try:
        main_spec.loader.exec_module(module)
        test_spec = importlib.util.spec_from_file_location("test_" + module_name, project / "test_main.py")
        if test_spec is None or test_spec.loader is None:
            errors.append(f"Cannot load test_main.py for {project.name}")
            continue
        test_module = importlib.util.module_from_spec(test_spec)
        test_spec.loader.exec_module(test_module)
        project_suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
        suite.addTests(project_suite)
    except Exception as exc:
        errors.append(f"Import error in {project.name}: {type(exc).__name__}: {exc}")
    finally:
        sys.path.remove(str(project))
        sys.modules.pop("main", None)

if old_main is not None:
    sys.modules["main"] = old_main
else:
    sys.modules.pop("main", None)

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)
if errors:
    print("\nLoad errors:")
    for err in errors:
        print(" -", err)
if errors or not result.wasSuccessful() or len(projects) != 100:
    print(f"Project folders found: {len(projects)} (expected 100)")
    raise SystemExit(1)
print(f"PASS: {result.testsRun} tests across {len(projects)} standalone projects.")
