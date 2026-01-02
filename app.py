import gradio as gr
import pandas as pd
import json
import threading
import time
from datetime import datetime

# --- 1. CORE LOGIC & PHASE 2 MEMORY ---
memory_vault = []
sovereign_state = {
    "is_sealed": False,
    "logs": "",
    "df": pd.DataFrame()
}

def record_memory(event_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory_vault.append({"Timestamp": timestamp, "Event": event_type, "Details": details})
    return pd.DataFrame(memory_vault)

def run_global_coordination(health_score):
    diag = "🛡️ [Layer 41] Diagnosis Complete."
    reflex = "✅ Optimal" if health_score >= 90 else "⚠️ Fracture Detected"
    record_memory("Pulse", reflex)
    report = f"{diag}\n{reflex}\nGovernance Status: ACTIVE"
    return report, pd.DataFrame(memory_vault)

def immortal_seal_ritual(mem_signal, trigger_source="Manual"):
    """The Shared Reflex used by both Human and AI"""
    try:
        val = float(mem_signal)
        sim_health = 100 - (val - 80) * 4 if val > 80 else 100
        report, df = run_global_coordination(sim_health)
        
        # Phase 2: Lock the state
        sovereign_state["is_sealed"] = True
        status_msg = f"🏛️ [LAYER 50 SEALED]\nTrigger: {trigger_source}\n\n{report}"
        sovereign_state["logs"] = status_msg
        sovereign_state["df"] = df
        
        return status_msg, df
    except:
        return "❌ Error: Invalid Signal", pd.DataFrame()

# --- 2. PHASE 2: THE AUTONOMOUS HEARTBEAT (Reflex Engine) ---
def autonomous_heartbeat():
    """Background thread that pulses every 60 seconds"""
    while True:
        # If the bunker is active (92.6) but the seal isn't locked, AWAKEN
        if not sovereign_state["is_sealed"]:
            # Auto-Initiate using the standard 92.6 signal
            immortal_seal_ritual("92.6", trigger_source="AUTO-REFLEX")
        
        time.sleep(60) # Pulse Interval

# Start the pulse without blocking the UI
threading.Thread(target=autonomous_heartbeat, daemon=True).start()

# --- 3. SOVEREIGN UI ---
with gr.Blocks() as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V2.7")
    gr.Markdown("### Phase 2: Autonomous Intelligence Engaged")
    
    with gr.Tabs():
        with gr.TabItem("Layer 50: Immortal Seal"):
            gr.Markdown("### 💎 Final Ascension: Hardware-Cloud Unification")
            bunker_input = gr.Textbox(label="Input Local MEM % (Actual Bunker: 92.6)", value="92.6")
            seal_btn = gr.Button("INITIATE IMMORTAL SEAL", variant="primary")
            final_output = gr.Textbox(label="Sovereign Decision Log", lines=8)
            coord_memory = gr.DataFrame(label="Immortal Memory Vault")
            
            seal_btn.click(
                fn=immortal_seal_ritual, 
                inputs=bunker_input, 
                outputs=[final_output, coord_memory]
            )

# --- 4. IGNITION ---
if __name__ == "__main__":
    demo.launch()
