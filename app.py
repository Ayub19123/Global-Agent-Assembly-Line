import gradio as gr
import pandas as pd
import threading
import time
import os
from datetime import datetime

# --- 1. CONFIG & MOTIF DICTIONARY ---
LEDGER_FILE = "Sovereign_Ledger.csv"
MOTIF_MAP = {
    "AUTO-REFLEX": ["#autonomy", "#reflexloop", "#selfgoverning"],
    "SEAL_INITIATED": ["#activation", "#sovereignmoment", "#finality"],
    "Pulse": ["#heartbeat", "#persistence", "#monitoring"],
    "STRESS_DETECTED": ["#resilience", "#load", "#pressureevent"],
    "GUARDIAN_ALERT": ["#selfhealing", "#auditloop", "#stabilitywatch"]
}

memory_vault = []
sovereign_state = {"is_sealed": False, "logs": "", "df": pd.DataFrame()}

# --- 2. THE MEANING ENGINE (Layer 55 Logic) ---
def annotate_with_motifs(event_type):
    """Attaches semantic tags based on event category"""
    motifs = MOTIF_MAP.get(event_type, ["#unclassified"])
    return " ".join(motifs)

def record_memory(event_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Timestamp": timestamp, "Event": event_type, "Details": details}
    
    memory_vault.append(entry)
    ledger_df = pd.DataFrame([entry])
    if not os.path.isfile(LEDGER_FILE):
        ledger_df.to_csv(LEDGER_FILE, index=False)
    else:
        ledger_df.to_csv(LEDGER_FILE, mode='a', header=False, index=False)
    return pd.DataFrame(memory_vault)

def extract_motif_signals(n=10):
    """Layer 55: Extracts signals with semantic meaning tags"""
    if os.path.exists(LEDGER_FILE):
        df = pd.read_csv(LEDGER_FILE)
        df_tail = df.tail(n).iloc[::-1]
        
        output = "🔮 SOVEREIGN MOTIF BROADCAST\n"
        output += "----------------------------\n"
        for _, row in df_tail.iterrows():
            motifs = annotate_with_motifs(row['Event'])
            output += f"[{row['Timestamp']}] {row['Event']} — {motifs}\n>> {row['Details']}\n\n"
        return output
    return "📡 Archive Empty: The Oracle is silent."

def refresh_sovereign_ledger():
    if os.path.exists(LEDGER_FILE):
        return pd.read_csv(LEDGER_FILE).iloc[::-1]
    return pd.DataFrame(columns=["Timestamp", "Event", "Details"])

def immortal_seal_ritual(mem_signal, trigger_source="Manual"):
    try:
        val = float(mem_signal)
        status = "✅ Optimal" if val <= 92.6 else "⚠️ Stress Detected"
        record_memory("SEAL_INITIATED" if trigger_source=="Manual" else "AUTO-REFLEX", 
                      f"Source: {trigger_source} | Signal: {mem_signal} | Status: {status}")
        sovereign_state["is_sealed"] = True
        return f"🏛️ [LAYER 50 SEALED]\nTrigger: {trigger_source}\n{status}", pd.DataFrame(memory_vault)
    except Exception as e:
        return f"❌ Error: {str(e)}", pd.DataFrame()

# --- 3. THE AUTONOMOUS HEARTBEAT ---
def autonomous_heartbeat():
    while True:
        if not sovereign_state["is_sealed"]:
            immortal_seal_ritual("92.6", trigger_source="AUTO-REFLEX")
        time.sleep(60)

threading.Thread(target=autonomous_heartbeat, daemon=True).start()

# --- 4. SOVEREIGN UI V2.9 ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V2.9")
    gr.Markdown("### Phase 2: Sovereign Meaning Engine (Layer 55) Active")
    
    with gr.Tabs():
        with gr.TabItem("Layer 50: Immortal Seal"):
            bunker_input = gr.Textbox(label="Input Local MEM % (Actual Bunker: 92.6)", value="92.6")
            seal_btn = gr.Button("INITIATE IMMORTAL SEAL", variant="primary")
            final_output = gr.Textbox(label="Sovereign Decision Log", lines=5)
            seal_btn.click(fn=immortal_seal_ritual, inputs=bunker_input, outputs=[final_output, gr.DataFrame()])

        with gr.TabItem("Layer 53: Sovereign Audit"):
            refresh_btn = gr.Button("SYNC AUDIT LEDGER")
            audit_table = gr.DataFrame(label="Live Disk-Record")
            refresh_btn.click(fn=refresh_sovereign_ledger, outputs=audit_table)

        with gr.TabItem("Layer 55: Motif Indexer"):
            gr.Markdown("### 🔮 Motif-Enhanced Global Echo")
            motif_btn = gr.Button("GENERATE MOTIF SIGNALS", variant="primary")
            motif_box = gr.Textbox(label="Semantic Broadcast Stream", lines=12)
            motif_btn.click(fn=extract_motif_signals, outputs=motif_box)

if __name__ == "__main__":
    demo.launch()
