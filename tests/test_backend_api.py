import pytest
from fastapi.testclient import TestClient

from backend.main import app
from simulation.generators.allocation_data import generate_allocation_scenario
from simulation.generators.dispatch_data import generate_dispatch_scenario

client = TestClient(app)


def test_health_and_root_endpoints():
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json() == {"status": "ok", "service": "FRADMS API"}

    r_root = client.get("/")
    assert r_root.status_code == 200
    data = r_root.json()
    assert "service" in data
    assert data["status"] == "healthy"


def test_allocation_endpoints_greedy_fair_compare():
    donations, agencies = generate_allocation_scenario(5, 3, seed=42)
    payload = {
        "donations": [d.model_dump(mode="json") for d in donations],
        "agencies": [a.model_dump(mode="json") for a in agencies],
    }

    # 1. Greedy
    r_greedy = client.post("/api/v1/allocation/greedy", json=payload)
    assert r_greedy.status_code == 200
    data_g = r_greedy.json()
    assert "Greedy Allocation" in data_g["algorithm"]
    assert "total_allocated" in data_g
    assert "jain_fairness_index" in data_g

    # 2. Fair
    r_fair = client.post("/api/v1/allocation/fair", json=payload)
    assert r_fair.status_code == 200
    data_f = r_fair.json()
    assert "Fairness-Aware Allocation" in data_f["algorithm"]

    # 3. Compare
    r_comp = client.post("/api/v1/allocation/compare", json=payload)
    assert r_comp.status_code == 200
    data_c = r_comp.json()
    assert "greedy" in data_c
    assert "fairness_aware" in data_c
    assert "comparison_summary" in data_c


def test_dispatch_endpoints_nearest_scored_batch_compare():
    reqs, vols = generate_dispatch_scenario(6, 4, seed=42)
    payload = {
        "requests": [r.model_dump(mode="json") for r in reqs],
        "volunteers": [v.model_dump(mode="json") for v in vols],
    }

    # 1. Nearest
    r_near = client.post("/api/v1/dispatch/nearest", json=payload)
    assert r_near.status_code == 200
    assert "Nearest Volunteer" in r_near.json()["algorithm"]

    # 2. Scored
    r_scored = client.post("/api/v1/dispatch/scored", json=payload)
    assert r_scored.status_code == 200
    assert "Score" in r_scored.json()["algorithm"]

    # 3. Batch
    r_batch = client.post("/api/v1/dispatch/batch", json=payload)
    assert r_batch.status_code == 200
    assert "Batch Bipartite" in r_batch.json()["algorithm"]

    # 4. Compare
    r_comp = client.post("/api/v1/dispatch/compare", json=payload)
    assert r_comp.status_code == 200
    data_c = r_comp.json()
    assert "nearest" in data_c
    assert "scored" in data_c
    assert "batch_bipartite" in data_c
    assert "comparison_summary" in data_c


def test_quick_simulation_endpoint():
    r_sim = client.post("/api/v1/simulation/quick", json={"sizes": [10, 25], "seed": 42})
    assert r_sim.status_code == 200
    data = r_sim.json()
    assert data["status"] == "success"
    assert len(data["allocation_results"]) > 0
    assert len(data["dispatch_results"]) > 0
    assert len(data["plots_generated"]) == 7


def test_api_validation_errors():
    # Empty lists return 400 Bad Request
    r_bad = client.post("/api/v1/allocation/greedy", json={"donations": [], "agencies": []})
    assert r_bad.status_code == 400
    assert "cannot be empty" in r_bad.json()["detail"]

    # Malformed schema returns 422 Unprocessable Entity
    r_malformed = client.post("/api/v1/allocation/greedy", json={"donations": "invalid"})
    assert r_malformed.status_code == 422
    data = r_malformed.json()
    assert data["error"] is True
    assert "message" in data


def test_engine_integration_pipeline():
    """Integration test verifying exact match between API response and underlying engine result."""
    donations, agencies = generate_allocation_scenario(4, 2, seed=99)
    payload = {
        "donations": [d.model_dump(mode="json") for d in donations],
        "agencies": [a.model_dump(mode="json") for a in agencies],
    }

    res = client.post("/api/v1/allocation/fair", json=payload)
    assert res.status_code == 200
    api_data = res.json()

    from engine.allocation.fair import FairnessAwareAllocator
    engine_res = FairnessAwareAllocator().allocate(donations, agencies)

    assert api_data["total_allocated"] == engine_res.total_allocated
    assert api_data["unmet_demand"] == engine_res.total_unmet_demand
    assert abs(api_data["jain_fairness_index"] - engine_res.jain_fairness_index) < 1e-3
