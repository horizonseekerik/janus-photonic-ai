
import re

with open("PROJECT_JANUS_STRATEGIC_ROADMAP.md", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Fix Model 6A Link Budget (18-stage instead of 17-stage)
text = text.replace(
    "Passive Split Tree (17-stage 2-Phase Time-Multiplexed Distribution):** $L_{\\text{split,ideal}} = \\mathbf{51.17\\text{ dB}}$",
    "Passive Split Tree (18-stage 2-Phase Time-Multiplexed Distribution):** $L_{\\text{split,ideal}} = 10\\log_{10}(2^{18}) = \\mathbf{54.18\\text{ dB}}$"
)
text = text.replace(
    "Total Optical Distribution Loss ($L_{\\text{total}}$):** $51.17\\text{ dB} + 16.45\\text{ dB} = \\mathbf{67.62\\text{ dB}}$",
    "Total Optical Distribution Loss ($L_{\\text{total}}$):** $54.18\\text{ dB} + 16.45\\text{ dB} = \\mathbf{70.63\\text{ dB}}$"
)

# 2. Add Link Budget for Model 6B
mod6b_budget = """#### 3. Optical Link Budget & Laser Requirement ($1064\\text{ nm}$)
* **Passive Split Tree (19-stage 2-Phase Time-Multiplexed Distribution):** $L_{\\text{split,ideal}} = 10\\log_{10}(2^{19}) = \\mathbf{57.19\\text{ dB}}$
* **Excess Path Loss ($L_{\\text{excess}}$):** $4.25\\text{ dB (MMIs)} + 7.50\\text{ dB (Bene\u0161)} + 4.00\\text{ dB (5x Interlayer)} + 1.60\\text{ dB (Prop/Cpl)} = \\mathbf{17.35\\text{ dB}}$
* **Total Optical Distribution Loss ($L_{\\text{total}}$):** $57.19\\text{ dB} + 17.35\\text{ dB} = \\mathbf{74.54\\text{ dB}}$
* **Delivered Receiver Power / Sensitivity:** $P_{\\text{det}} = \\mathbf{-21.54\\text{ dBm}}$ | $P_{\\text{sens}} = \\mathbf{-23.20\\text{ dBm}}$ (Margin = $+1.66\\text{ dB}$)
* **Master Laser Optical Power ($P_{\\text{laser,opt}}$):** $\\mathbf{200.00\\text{ W Optical CW}}$ ($+53.0\\text{ dBm}$)
* **Laser Wall-Plug Electrical Power ($>75\\%$ WPE):** $\\mathbf{266.67\\text{ Watts}}$"""

text = re.sub(
    r"#### 3\. Optical Link Budget & Laser Requirement \(\$1064\\text\{ nm\}\$\)\n\* \*\*Master Laser Optical Power.+?\\mathbf\{266\.67\\text\{ Watts\}\}\$",
    mod6b_budget.replace("\\", "\\\\"),
    text,
    flags=re.MULTILINE | re.DOTALL
)


# 3. Add Customer Perspective Section before the Matrix
customer_perspective = """
## 8. Product Positioning & Customer Perspective: Edge 16-Tile vs. Mini 64-Tile

A common architectural question arises when evaluating the **Edge 16-Tile** and the **Mini 64-Tile** models. Both feature exactly **65,536 optical multipliers**, consume **23.29 W** of power, and occupy **$200\\text{ mm}^2$** of silicon area (in their 2-Stratum and 3-Stratum incarnations respectively). However, they serve completely divergent customer profiles:

### The Mini 64-Tile ($32 \\times 32$ per tile)
* **Customer Profile:** Robotics, Autonomous Vehicles (AV), and multi-sensor IoT edge nodes.
* **Workload Dynamics:** Requires executing many smaller, independent neural networks simultaneously. For example, an AV might need to process 8 radar streams, 4 lidar feeds, and 12 camera feeds at once.
* **Advantage:** The 64 independent tiles allow the OS scheduler to achieve **massive multi-tenancy**. The customer can map 64 independent $32 \\times 32$ matrix workloads in parallel without them blocking each other, achieving true spatial multitasking.

### The Edge 16-Tile ($64 \\times 64$ per tile)
* **Customer Profile:** Local LLM Inference (e.g., LLaMA-3 8B), on-premise generative AI, and heavy monolithic signal processing.
* **Workload Dynamics:** Requires executing singular, massive dense matrix multiplications (GEMMs). 
* **Advantage:** The $64 \\times 64$ matrix dimension allows for **4x larger contiguous matrix multiplications** per cycle per tile. This drastically reduces the software compiler overhead and memory-fetch bottlenecks associated with slicing massive LLM weight matrices into tiny $32 \\times 32$ blocks. 

---
"""

text = text.replace("## 1. Executive Mission & Generational Strategy", customer_perspective + "\n## 1. Executive Mission & Generational Strategy")

# Wait, putting it before Section 1 is weird. Let us append it to the Executive Mission or a dedicated section at the end.
# Actually, I will place it right after the Generation Matrix.
text = text.replace(customer_perspective + "\n## 1. Executive Mission & Generational Strategy", "## 1. Executive Mission & Generational Strategy")

idx = text.find("## 2. Generation 1")
text = text[:idx] + customer_perspective + "\n\n" + text[idx:]

# Ensure Beneš renders correctly
text = text.replace("Bene", "Beneš").replace("Bene?", "Beneš")

with open("PROJECT_JANUS_STRATEGIC_ROADMAP.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Markdown file successfully updated.")

