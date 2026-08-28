"""
PROJECT JANUS MINI (16-TILE): INTERACTIVE DASHBOARD HTTP SERVER
===============================================================
Threaded HTTP server providing robust local visual exploration of the
JANUS multi-physics co-simulation stack, optical routing, and GPU comparisons.
Includes automatic shutdown when the browser tab/window is closed.
"""

import sys
import os
import json
import time
import threading
import http.server
import urllib.parse
from typing import Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Redirect stdout and stderr to a log file when running under windowless pythonw.exe
LOG_PATH = os.path.join(BASE_DIR, "dashboard.log")
if sys.stdout is None:
    sys.stdout = open(LOG_PATH, "a", encoding="utf-8", buffering=1)
if sys.stderr is None:
    sys.stderr = open(LOG_PATH, "a", encoding="utf-8", buffering=1)

from orchestrator.master_orchestrator import JanusMasterOrchestrator
from tier5_python_rns.ai_workload_benchmarks import AIWorkloadProfiler
from tier5_python_rns.gpu_comparator import GPUComparator
from tier5_python_rns.batch_token_packer import BatchTokenPacker
from tier5_python_rns.jir_thermal_scheduler import JIRThermalScheduler
from tier3_xyce_circuit.eye_diagram_ber import EyeDiagramAndBERSolver

# Global Heartbeat & Watchdog State
LAST_HEARTBEAT = time.time()
HEARTBEAT_INITIALIZED = False


def heartbeat_watchdog():
    """Background watchdog thread that auto-terminates the server if no browser tab is open."""
    while True:
        time.sleep(5)
        # 300 seconds (5 minutes) grace period to allow reading and downloading without premature exit
        if HEARTBEAT_INITIALIZED and (time.time() - LAST_HEARTBEAT > 300.0):
            os._exit(0)


# Start watchdog thread
watchdog_thread = threading.Thread(target=heartbeat_watchdog, daemon=True)
watchdog_thread.start()


class JanusDashboardHandler(http.server.BaseHTTPRequestHandler):
    """Threaded HTTP handler with proper headers and auto-shutdown capabilities."""

    _orchestrator = None
    _ai_profiler = None
    _gpu_comp = None
    _token_packer = None

    @classmethod
    def get_orchestrator(cls):
        if cls._orchestrator is None:
            cls._orchestrator = JanusMasterOrchestrator(verbose=False)
        return cls._orchestrator

    @classmethod
    def get_profiler(cls):
        if cls._ai_profiler is None:
            cls._ai_profiler = AIWorkloadProfiler()
        return cls._ai_profiler

    @classmethod
    def get_gpu_comp(cls):
        if cls._gpu_comp is None:
            cls._gpu_comp = GPUComparator()
        return cls._gpu_comp

    @classmethod
    def get_token_packer(cls):
        if cls._token_packer is None:
            cls._token_packer = BatchTokenPacker()
        return cls._token_packer

    def log_message(self, format, *args):
        if sys.stderr is not None:
            try:
                sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))
            except Exception:
                pass

    def send_json_response(self, data: Any, status: int = 200):
        def json_default(obj):
            if hasattr(obj, "item"):
                return obj.item()
            if hasattr(obj, "tolist"):
                return obj.tolist()
            return str(obj)
        body = json.dumps(data, default=json_default).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def trigger_shutdown(self):
        """Cleanly terminates the server process after responding."""
        threading.Timer(0.3, lambda: os._exit(0)).start()

    def do_GET(self):
        global LAST_HEARTBEAT, HEARTBEAT_INITIALIZED
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Update heartbeat on any GET request
        LAST_HEARTBEAT = time.time()
        HEARTBEAT_INITIALIZED = True

        if path in ["/", "/index.html"]:
            html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        elif path == "/api/heartbeat":
            self.send_json_response({"status": "alive", "timestamp": time.time()})
            return

        elif path == "/api/shutdown":
            self.send_json_response({"status": "shutting_down"})
            self.trigger_shutdown()
            return

        elif path == "/api/matrix_data":
            orc = self.get_orchestrator()
            if not orc.checks:
                res = orc.run_full_cosim()
                self.send_json_response({"checks": res.get("checks", []), "overall_pass": res.get("overall_pass", True), "summary": res.get("summary", {})})
            else:
                self.send_json_response({"checks": [c.__dict__ for c in orc.checks], "overall_pass": orc.overall_pass, "summary": {"passed": sum(1 for c in orc.checks if c.passed), "total": len(orc.checks)}})
            return

        elif path == "/api/run_single_check":
            query = urllib.parse.parse_qs(parsed.query)
            check_id = int(query.get("id", [1])[0])
            res = self.get_orchestrator().run_single_check(check_id)
            self.send_json_response(res)
            return

        elif path == "/api/run_tier":
            query = urllib.parse.parse_qs(parsed.query)
            tier_id = int(query.get("tier", [1])[0])
            res = self.get_orchestrator().run_tier(tier_id)
            self.send_json_response(res)
            return

        elif path == "/api/full_cosim":
            res = self.get_orchestrator().run_full_cosim()
            self.send_json_response(res)
            return

        elif path == "/api/ai_benchmarks":
            llama_res = self.get_profiler().benchmark_llama3_8b(batch_size=1, seq_len=1, precision="INT8")
            gpt_res = self.get_profiler().benchmark_gpt2_base(batch_size=1, seq_len=1, precision="INT8")
            vit_res = self.get_profiler().benchmark_vit_huge(batch_size=1, precision="INT8")
            hw_comp = self.get_gpu_comp().get_hardware_comparison_table()
            attn_pack = self.get_token_packer().pack_multihead_attention(num_heads=32, d_head=128, seq_len=64, precision="INT8")
            mlp_pack = self.get_token_packer().pack_batch_mlp(batch_size=32, hidden_dim=4096, intermediate_dim=14336, precision="INT8")

            payload = {
                "llama3": llama_res,
                "gpt2": gpt_res,
                "vit": vit_res,
                "gpu_comparison": hw_comp,
                "attention_packing": attn_pack.__dict__,
                "mlp_packing": mlp_pack.__dict__,
            }
            self.send_json_response(payload)
            return

        elif path == "/api/thermal_data":
            scheduler = JIRThermalScheduler()
            sim_res = scheduler.run_workload_simulation(total_epochs=100)
            sample_traces = [list(h) for h in scheduler.temp_history[:50]]
            payload = {
                "max_temperature_C": sim_res["max_temperature_C"],
                "thermal_violations": sim_res["thermal_violations"],
                "traces": sample_traces,
                "final_temps": [float(t) for t in scheduler.temperatures],
            }
            self.send_json_response(payload)
            return

        elif path in ["/api/pdf", "/paper.pdf", "/main.pdf"]:
            query = urllib.parse.parse_qs(parsed.query)
            is_download = query.get("download", ["0"])[0] == "1"
            pdf_candidates = [
                os.path.join(os.path.dirname(__file__), "main.pdf"),
                os.path.join(BASE_DIR, "dashboard", "main.pdf"),
                os.path.abspath(os.path.join(BASE_DIR, "..", "paper_latex", "main.pdf")),
            ]
            pdf_path = next((p for p in pdf_candidates if os.path.isfile(p)), None)
            if pdf_path:
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_data = f.read()
                    disposition_type = "attachment" if is_download else "inline"
                    self.send_response(200)
                    self.send_header("Content-Type", "application/pdf")
                    self.send_header("Content-Length", str(len(pdf_data)))
                    self.send_header("Content-Disposition", f"{disposition_type}; filename=JANUS_IEEE_Manuscript.pdf")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Cache-Control", "no-cache, must-revalidate")
                    self.end_headers()
                    self.wfile.write(pdf_data)
                    return
                except Exception as e:
                    self.send_json_response({"error": str(e)}, status=500)
                    return
            else:
                self.send_json_response({"error": "PDF manuscript not found"}, status=404)
                return

        elif path in ["/api/simulation_pdf", "/simulation_report.pdf"]:
            query = urllib.parse.parse_qs(parsed.query)
            is_download = query.get("download", ["0"])[0] == "1"
            sim_pdf_candidates = [
                os.path.join(BASE_DIR, "dashboard", "JANUS_Mini16_Simulation_Report.pdf"),
                os.path.abspath(os.path.join(BASE_DIR, "..", "simulation_paper_latex", "JANUS_Mini16_Detailed_Simulation_Report.pdf")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "documentation_reports", "JANUS_Mini16_Simulation_Report.pdf")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "simulation_paper_latex", "JANUS_Mini16_Simulation_Report_v2.pdf")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "simulation_paper_latex", "JANUS_Mini16_Simulation_Report.pdf")),
                os.path.join(BASE_DIR, "dashboard", "simulation_report.pdf"),
            ]
            pdf_path = next((p for p in sim_pdf_candidates if os.path.isfile(p)), None)
            if pdf_path:
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_data = f.read()
                    disposition_type = "attachment" if is_download else "inline"
                    self.send_response(200)
                    self.send_header("Content-Type", "application/pdf")
                    self.send_header("Content-Length", str(len(pdf_data)))
                    self.send_header("Content-Disposition", f"{disposition_type}; filename=JANUS_Mini16_Simulation_Report.pdf")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Cache-Control", "no-cache, must-revalidate")
                    self.end_headers()
                    self.wfile.write(pdf_data)
                    return
                except Exception as e:
                    self.send_json_response({"error": str(e)}, status=500)
                    return
            else:
                self.send_json_response({"error": "Simulation PDF report not found"}, status=404)
                return

        elif path in ["/api/cmos_pdf", "/cmos_paper.pdf", "/cmos_architecture.pdf", "/JANUS_Mini16_CMOS_Architecture.pdf"]:
            query = urllib.parse.parse_qs(parsed.query)
            is_download = query.get("download", ["0"])[0] == "1"
            cmos_pdf_candidates = [
                os.path.join(BASE_DIR, "dashboard", "JANUS_Mini16_CMOS_Architecture.pdf"),
                os.path.abspath(os.path.join(BASE_DIR, "..", "cmos_paper_latex", "JANUS_Mini16_CMOS_Architecture.pdf")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "documentation_reports", "JANUS_Mini16_CMOS_Architecture.pdf")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "JANUS_Mini16_CMOS_Architecture.pdf")),
                os.path.join(BASE_DIR, "dashboard", "cmos_architecture.pdf"),
            ]
            pdf_path = next((p for p in cmos_pdf_candidates if os.path.isfile(p)), None)
            if pdf_path:
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_data = f.read()
                    disposition_type = "attachment" if is_download else "inline"
                    self.send_response(200)
                    self.send_header("Content-Type", "application/pdf")
                    self.send_header("Content-Length", str(len(pdf_data)))
                    self.send_header("Content-Disposition", f"{disposition_type}; filename=JANUS_Mini16_CMOS_Architecture.pdf")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Cache-Control", "no-cache, must-revalidate")
                    self.end_headers()
                    self.wfile.write(pdf_data)
                    return
                except Exception as e:
                    self.send_json_response({"error": str(e)}, status=500)
                    return
            else:
                self.send_json_response({"error": "CMOS Architecture PDF not found"}, status=404)
                return

        elif path == "/api/codebase":
            query = urllib.parse.parse_qs(parsed.query)
            req_file = query.get("file", [None])[0]

            root_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))
            allowed_roots = [
                BASE_DIR,
                os.path.abspath(os.path.join(BASE_DIR, "..", "simulation_paper_latex")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "paper_latex")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "cmos_paper_latex")),
                os.path.abspath(os.path.join(BASE_DIR, "..", "documentation_reports")),
            ]

            if req_file:
                # Clean and resolve path
                safe_rel = os.path.normpath(req_file).lstrip("/\\")
                target_path = os.path.abspath(os.path.join(root_dir, safe_rel))
                
                # Security check: must reside in allowed roots
                if not any(target_path.startswith(ar) for ar in allowed_roots) or not os.path.isfile(target_path):
                    self.send_json_response({"error": "File not found or access denied"}, status=404)
                    return
                
                try:
                    with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                        code_text = f.read()
                    ext = os.path.splitext(target_path)[1].lower()
                    lang_map = {
                        ".py": "python", ".v": "verilog", ".sv": "systemverilog",
                        ".json": "json", ".html": "html", ".css": "css", ".js": "javascript",
                        ".tex": "latex", ".bib": "bibtex", ".md": "markdown", ".sif": "text", ".geo": "text"
                    }
                    self.send_json_response({
                        "file": safe_rel.replace("\\", "/"),
                        "name": os.path.basename(target_path),
                        "content": code_text,
                        "lines": len(code_text.splitlines()),
                        "language": lang_map.get(ext, "text"),
                        "size_bytes": os.path.getsize(target_path)
                    })
                    return
                except Exception as e:
                    self.send_json_response({"error": str(e)}, status=500)
                    return
            else:
                # Return categorized list of full multi-physics simulation, RTL, plotting, and paper source files
                tree = [
                    {
                        "category": "Tier 1: Optics & Photonics (MEEP FDTD)",
                        "tier": "tier1",
                        "files": [
                            {"name": "sb2s3_switch_cell.py", "path": "janus_mini16_sim/tier1_meep_optics/sb2s3_switch_cell.py", "desc": "3D FDTD of Sb2S3 PCM Directional Coupler Switch (0.010 dB Amorph, 0.096 dB Cryst)"},
                            {"name": "sb2s3_tolerance_monte_carlo.py", "path": "janus_mini16_sim/tier1_meep_optics/sb2s3_tolerance_monte_carlo.py", "desc": "2,000-Trial Statistical Monte Carlo Tolerance & Yield Engine"},
                            {"name": "waveguide_crossing.py", "path": "janus_mini16_sim/tier1_meep_optics/waveguide_crossing.py", "desc": "Analytical MMI Waveguide Crossing Model (0.0131 dB IL, -41.06 dB XT)"},
                            {"name": "litao3_pockels_router.py", "path": "janus_mini16_sim/tier1_meep_optics/litao3_pockels_router.py", "desc": "1x256 Electro-Optic Pockels Modulator Tree"},
                            {"name": "gds_layout_processor.py", "path": "janus_mini16_sim/tier1_meep_optics/gds_layout_processor.py", "desc": "GDSII Mask and Waveguide Density Synthesizer"}
                        ]
                    },
                    {
                        "category": "Tier 2: Thermal FEM & Multi-Stratum Stack (Elmer)",
                        "tier": "tier2",
                        "files": [
                            {"name": "elmer_thermal_solver.py", "path": "janus_mini16_sim/tier2_elmer_thermal/elmer_thermal_solver.py", "desc": "3D Monolithic FEM Thermal Solver & Boundary Validator"},
                            {"name": "gmsh_mesh_generator.py", "path": "janus_mini16_sim/tier2_elmer_thermal/gmsh_mesh_generator.py", "desc": "330 um Multi-Layer Active Stack 3D Mesh Generator"},
                            {"name": "extract_thermal_rom.py", "path": "janus_mini16_sim/tier2_elmer_thermal/extract_thermal_rom.py", "desc": "Reduced-Order Thermal Impedance Matrix Extractor"}
                        ]
                    },
                    {
                        "category": "Tier 3: Mixed-Signal Circuit & Noise (Xyce / SPICE)",
                        "tier": "tier3",
                        "files": [
                            {"name": "eye_diagram_ber.py", "path": "janus_mini16_sim/tier3_xyce_circuit/eye_diagram_ber.py", "desc": "100 GHz Eye Diagram, Jitter Variance & Dynamic BER Solver"},
                            {"name": "strongarm_latch.py", "path": "janus_mini16_sim/tier3_xyce_circuit/strongarm_latch.py", "desc": "Clocked StrongARM Regenerative Comparator Model"},
                            {"name": "ilo_comb_lock.py", "path": "janus_mini16_sim/tier3_xyce_circuit/ilo_comb_lock.py", "desc": "50 fs Injection-Locked Oscillator Comb Receiver Clock"},
                            {"name": "apd_receiver_model.py", "path": "janus_mini16_sim/tier3_xyce_circuit/apd_receiver_model.py", "desc": "Ge/Si SAC2M APD Model (M=7, 105 GHz BW)"}
                        ]
                    },
                    {
                        "category": "Tier 4: Digital RTL & CRT Synthesis",
                        "tier": "tier4",
                        "files": [
                            {"name": "rtl_synthesis_analyzer.py", "path": "janus_mini16_sim/tier4_rtl_digital/rtl_synthesis_analyzer.py", "desc": "Yosys RTL Synthesis Parser for CMOS CRT Logic"},
                            {"name": "test_crt_cocotb.py", "path": "janus_mini16_sim/tier4_rtl_digital/test_crt_cocotb.py", "desc": "Cocotb Hardware Verification Testbench"}
                        ]
                    },
                    {
                        "category": "Tier 5: Residue Number System & AI Benchmarks",
                        "tier": "tier5",
                        "files": [
                            {"name": "formal_verifier.py", "path": "janus_mini16_sim/tier5_python_rns/formal_verifier.py", "desc": "Formal Z3 SMT Mathematical Proofs for 64-Bit PRNS"},
                            {"name": "jir_thermal_scheduler.py", "path": "janus_mini16_sim/tier5_python_rns/jir_thermal_scheduler.py", "desc": "Just-In-Time Rotation (JIR) Dynamic Thermal Scheduler"},
                            {"name": "batch_token_packer.py", "path": "janus_mini16_sim/tier5_python_rns/batch_token_packer.py", "desc": "Multi-Head Attention & MLP Spatial Token Batching"},
                            {"name": "ai_workload_benchmarks.py", "path": "janus_mini16_sim/tier5_python_rns/ai_workload_benchmarks.py", "desc": "LLaMA-3 70B, GPT-4, and ViT-Huge Execution Profiler"},
                            {"name": "gemm_exact_benchmark.py", "path": "janus_mini16_sim/tier5_python_rns/gemm_exact_benchmark.py", "desc": "Exact INT4 to INT64 Matrix Multiplication Engine"},
                            {"name": "gpu_comparator.py", "path": "janus_mini16_sim/tier5_python_rns/gpu_comparator.py", "desc": "Throughput & Energy Scaling vs NVIDIA H100/B200"}
                        ]
                    },
                    {
                        "category": "Scientific Plotting & Benchmarks",
                        "tier": "benchmarks",
                        "files": [
                            {"name": "export_simulation_field_plots.py", "path": "janus_mini16_sim/benchmarks/export_simulation_field_plots.py", "desc": "Generates 3D MEEP Optics, Elmer Thermal Heatmaps, and Xyce Eye Diagrams"},
                            {"name": "run_ai_profiling.py", "path": "janus_mini16_sim/benchmarks/run_ai_profiling.py", "desc": "Frontier AI Model Throughput & Power Profiling Benchmark"}
                        ]
                    },
                    {
                        "category": "System Orchestration, Constants & Verification Suite",
                        "tier": "core",
                        "files": [
                            {"name": "mini_16t_constants.py", "path": "janus_mini16_sim/configs/mini_16t_constants.py", "desc": "Central Physical Constants and Parameter Registry"},
                            {"name": "master_orchestrator.py", "path": "janus_mini16_sim/orchestrator/master_orchestrator.py", "desc": "5-Tier Co-Simulation Orchestrator & Spec Auditor"},
                            {"name": "test_interactive_thermal.py", "path": "janus_mini16_sim/dashboard/test_interactive_thermal.py", "desc": "Interactive Multi-Tile Thermal & JIR Unit Test Suite"},
                            {"name": "test_prolonged_thermal.py", "path": "janus_mini16_sim/dashboard/test_prolonged_thermal.py", "desc": "1-Hour & 24-Hour Continuous Datacenter Stress Test Suite"}
                        ]
                    }
                ]
                self.send_json_response({"tree": tree})
                return

        # 404 Fallback
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        msg = b"Not Found"
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)

    def do_POST(self):
        global LAST_HEARTBEAT, HEARTBEAT_INITIALIZED
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"

        LAST_HEARTBEAT = time.time()
        HEARTBEAT_INITIALIZED = True

        if path == "/api/shutdown":
            self.send_json_response({"status": "shutting_down"})
            self.trigger_shutdown()
            return

        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if path == "/api/eval_val":
            val_str = str(data.get("val", "0")).strip().replace("_", "").replace(",", "")
            val = int(val_str, 16) if (val_str.lower().startswith("0x") or val_str.lower().startswith("-0x") or val_str.lower().startswith("+0x")) else int(val_str, 10)
            res = self.get_orchestrator().evaluate_custom_integer(val, print_output=False)
            self.send_json_response(res)
            return

        elif path == "/api/eval_mult":
            a_str = str(data.get("a", "0")).strip().replace("_", "").replace(",", "")
            b_str = str(data.get("b", "0")).strip().replace("_", "").replace(",", "")
            a = int(a_str, 16) if (a_str.lower().startswith("0x") or a_str.lower().startswith("-0x") or a_str.lower().startswith("+0x")) else int(a_str, 10)
            b = int(b_str, 16) if (b_str.lower().startswith("0x") or b_str.lower().startswith("-0x") or b_str.lower().startswith("+0x")) else int(b_str, 10)
            res = self.get_orchestrator().evaluate_custom_multiply(a, b, print_output=False)
            self.send_json_response(res)
            return

        elif path == "/api/run_custom_thermal_sim":
            active_count = int(data.get("num_active_tiles", 4))
            intensity = str(data.get("intensity", "high"))
            duration_val = float(data.get("duration_val", 1.0))
            duration_unit = str(data.get("duration_unit", "hours"))
            threshold_c = float(data.get("threshold_c", 40.0))
            jir_enabled = bool(data.get("jir_enabled", True))
            scheduler = JIRThermalScheduler()
            sim_res = scheduler.run_custom_workload_simulation(
                active_tile_count=active_count,
                intensity=intensity,
                duration_val=duration_val,
                duration_unit=duration_unit,
                rotation_threshold_C=threshold_c,
                jir_enabled=jir_enabled
            )
            self.send_json_response(sim_res)
            return

        elif path == "/api/tile_specs":
            tile_id = int(data.get("tile_id", 0))
            temp_c = float(data.get("temp_c", 25.0)) if "temp_c" in data else None
            state = str(data.get("state", "ACTIVE"))
            activations = data.get("activations_count")
            duty_pct = data.get("duty_cycle_pct")
            active_time_str = data.get("active_time_formatted")
            scheduler = JIRThermalScheduler()
            specs = scheduler.get_tile_detailed_physical_specs(
                tile_id,
                temperature_C=temp_c,
                state=state,
                activations_count=int(activations) if activations is not None else None,
                duty_cycle_pct=float(duty_pct) if duty_pct is not None else None,
                active_time_formatted=str(active_time_str) if active_time_str is not None else None,
            )
            self.send_json_response(specs)
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        msg = b"Not Found"
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)


def start_dashboard_server(port: int = 8080):
    """Starts the multi-threaded JANUS interactive dashboard server."""
    os.chdir(BASE_DIR)
    server_address = ("127.0.0.1", port)
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer(server_address, JanusDashboardHandler) as httpd:
        if sys.stdout is not None:
            try:
                print(f"\n======================================================================")
                print(f"  PROJECT JANUS: INTERACTIVE VISUAL DASHBOARD ACTIVE")
                print(f"  Local URL : http://127.0.0.1:{port}/")
                print(f"  Auto-Shutdown enabled on browser tab closure")
                print(f"======================================================================\n")
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            if sys.stdout is not None:
                print("\nDashboard server stopped.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="JANUS Dashboard Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()
    start_dashboard_server(port=args.port)
