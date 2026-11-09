"""Run all project stages in sequence. Use this after installing requirements."""
from src.data_pipeline import audit,clean_data,validate
from src.customer_models import rfm_and_segments,build_lapse_model
from src.triage import run_pipeline,FEW
from src.policy_rag import PolicyRAG,evaluate
def main():
    print("\n=== PART A: AUDIT / CLEAN / VALIDATE ===")
    audit(); clean_data(); validate()
    print("\n=== PART B: SEGMENTS ===")
    rfm,diagnostics,profile,pca=rfm_and_segments()
    print("K-means diagnostics:\n",diagnostics.to_string(index=False))
    print("Segment profile:\n",profile.to_string(index=False)); print("PCA explained variance:",pca)
    print("Lapse model summary:",build_lapse_model())
    print("\n=== PART C: TRIAGE ===")
    triage,summary=run_pipeline(prompt=FEW,token_budget=100000)
    print(summary); print(triage.head().to_string(index=False))
    print("\n=== PART D: POLICY RAG ===")
    rag=PolicyRAG(); print("chunks:",len(rag.chunks)); print(evaluate(rag).to_string(index=False))
    print("\n=== PART D: REFUND CO-PILOT ===")
    import sqlite3
    from src.data_pipeline import DB
    from src.refund_agent import run_agent
    with sqlite3.connect(DB) as con:
        late=con.execute("SELECT order_id FROM orders WHERE status='completed' AND delivery_minutes>45 LIMIT 1").fetchone()[0]
    print(run_agent(f"Refund order {late}",scenario_id="run-project-demo")["final_answer"])
    print("\nProject pipeline finished. Review outputs/ and data/instamart.db.")
if __name__=="__main__": main()
