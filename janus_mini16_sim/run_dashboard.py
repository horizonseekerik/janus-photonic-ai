#!/usr/bin/env python3
"""
PROJECT JANUS MINI (16-TILE): DASHBOARD LAUNCHER
=================================================
Launches the local interactive web visualizer on http://localhost:8080.

Usage:
    python run_dashboard.py
    python run_dashboard.py --port 8501
"""

import sys
import os
import argparse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dashboard.server import start_dashboard_server


def main():
    parser = argparse.ArgumentParser(description="Launch Project JANUS Interactive Web Dashboard")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve dashboard on (default: 8080)")
    args = parser.parse_args()

    start_dashboard_server(port=args.port)


if __name__ == "__main__":
    main()
