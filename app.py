import gradio as gr
import pandas as pd
import json
import threading
import time
import os
from datetime import datetime

# --- 1. SOVEREIGN MEMORY & LEDGER PATHS ---
LEDGER_FILE = "Sovereign_Ledger.csv"
memory_vault = []
sovereign_state = {
    "is_sealed": False,
    "logs": "",
    "df": pd.DataFrame()
}

def record_memory(event_type, details):
    """The Dual-Action Ledger: Records to RAM and Disk"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Timestamp": timestamp, "Event": event_type, "Details": details}
    
    # Action 1: In-Memory (for the UI)
    memory_vault.append(entry)
    df = pd.DataFrame(memory_vault)
    
    # Action 2: On-Disk (The Immutable Ledger)
    ledger_df = pd.DataFrame([entry])
    if not os.path.isfile(LEDGER_FILE):
        ledger_df.to_csv(LEDGER_FILE, index=False)
    else:
        ledger_df.to_csv(LEDGER_FILE, mode='a', header=False, index=False)
        
    return df

def refresh_sovereign_ledger():
    """Reads the disk-based CSV for the Audit Window"""
    if os.path.exists(LEDGER_FILE):
        ledger_df = pd.read_csv(LEDGER_FILE)
        return ledger_df.iloc[::-1]
    return pd.DataFrame(columns=["Timestamp", "Event", "Details"])

def extract_sovereign_signals():
    """Layer 54: Extracts broadcast-ready messages from the Ledger"""
    if os.path.exists(LEDGER_FILE):
        df = pd.read_csv(LEDGER_FILE)
        # Filter for high-value signals (Pulses and Seals)
        signals = df[df['Event'].isin(['SEAL_INITIATED', 'Pulse'])]
        latest_signals = signals.tail(5).iloc[::-1]
        
        output = "🚀 SOVEREIGN ARCHIVE BROADCAST\n"
        output += "----------------------------\n"
        for _, row in latest_signals.iterrows():
            motif = "🏛️" if row['Event'] == 'SEAL_INITIATED' else "📡"
            output += f"{motif} [{row['Timestamp']}] {row['Event']}: {row['Details']}\n"
        output += "\n🔗 Status: IMMORTAL SEAL ACTIVE"
        return output
    return "📡 Signal Loop search complete: No records found."

def run_global_coordination(health_score):
    diag = "🛡️ [Layer 41] Diagnosis Complete."
    reflex = "✅ Optimal" if health_score >= 90 else "⚠️ Stress Detected"
    df = record_memory("Pulse", reflex)
    report = f"{diag}\n{reflex}\nGovernance Status: ACTIVE"
    return report, df

def immortal_seal_ritual(mem_signal, trigger_source="Manual"):
    try:
        val = float(mem_signal)
        sim_health = 100 - (val - 80) * 4 if val > 80 else 100
        report, df = run_global_coordination(sim_health)
        
        sovereign_state["is_sealed"] = True
        status_msg = f"🏛️ [LAYER 50 SEALED]\nTrigger: {trigger_source}\n\n{report}"
        sovereign_state["logs"] = status_msg
        sovereign_state["df"] = df
        
        record_memory("SEAL_INITIATED", f"Source: {trigger_source} | Signal: {mem_signal}")
        
        return status_msg, df
    except Exception as e:
        return f"❌ Error: {str(e)}", pd.DataFrame()

# --- 2. THE AUTONOMOUS HEARTBEAT (Reflex Engine) ---
def autonomous_heartbeat():
    while True:
        if not sovereign_state["is_sealed"]:
            immortal_seal_ritual("92.6", trigger_source="AUTO-REFLEX")
        time.sleep(60)

threading.Thread(target=autonomous_heartbeat, daemon=True).start()

# --- 3. SOVEREIGN UI V2.8 (Broadcasting Enabled) ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V2.8")
    gr.Markdown("### Phase 2: Immutable Audit Ledger Active")
    
    with gr.Tabs():
        with gr.TabItem("Layer 50: Immortal Seal"):
            gr.Markdown("### 💎 Final Ascension: Hardware-Cloud Unification")
            bunker_input = gr.Textbox(label="Input Local MEM % (Actual Bunker: 92.6)", value="92.6")
            seal_btn = gr.Button("INITIATE IMMORTAL SEAL", variant="primary")
            final_output = gr.Textbox(label="Sovereign Decision Log", lines=8)
            coord_memory = gr.DataFrame(label="Session Memory (RAM Only)")
            
            seal_btn.click(fn=immortal_seal_ritual, inputs=bunker_input, outputs=[final_output, coord_memory])

        with gr.TabItem("Layer 53: Sovereign Audit"):
            gr.Markdown("### 📜 Immutable Ledger Audit Window")
            refresh_btn = gr.Button("SYNC AUDIT LEDGER", variant="secondary")
            audit_table = gr.DataFrame(label="Live Disk-Record (Historical Archive)")
            
            refresh_btn.click(fn=refresh_sovereign_ledger, outputs=audit_table)

        with gr.TabItem("Layer 54: Global Echo"):
            gr.Markdown("### 📡 Sovereign Signal Broadcast")
            gr.Markdown("Generate signals from the ledger for LinkedIn, X, or External Journals.")
            echo_btn = gr.Button("GENERATE GLOBAL ECHO", variant="primary")
            echo_output = gr.Textbox(label="Broadcast-Ready Signals", lines=10)
            
            echo_btn.click(fn=extract_sovereign_signals, outputs=echo_output)

# --- 4. IGNITION ---
if __name__ == "__main__":
    demo.launch()
