"""Django management command to run both frontend and backend servers."""

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style


class Command(BaseCommand):
    help = "Run both frontend (Vite) and backend (Django) development servers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--frontend-port",
            type=int,
            default=5173,
            help="Port for the frontend development server (default: 5173)",
        )
        parser.add_argument(
            "--backend-port",
            type=int,
            default=8000,
            help="Port for the backend development server (default: 8000)",
        )
        parser.add_argument(
            "--frontend-only",
            action="store_true",
            help="Run only the frontend server",
        )
        parser.add_argument(
            "--backend-only",
            action="store_true",
            help="Run only the backend server",
        )

    def handle(self, *args, **options):
        self.style = color_style()

        # Validate argument combinations
        if options["frontend_only"] and options["backend_only"]:
            raise CommandError("Cannot specify both --frontend-only and --backend-only")

        # Get the frontend directory path
        frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"

        if not frontend_dir.exists():
            raise CommandError(f"Frontend directory not found: {frontend_dir}")

        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            raise CommandError(f"package.json not found in {frontend_dir}")

        processes = []

        try:
            if not options["backend_only"]:
                # Start frontend server
                frontend_process = self._start_frontend_server(
                    frontend_dir, options["frontend_port"]
                )
                processes.append(("Frontend", frontend_process))

            if not options["frontend_only"]:
                # Start backend server
                backend_process = self._start_backend_server(options["backend_port"])
                processes.append(("Backend", backend_process))

            if not processes:
                raise CommandError("No processes to start")

            # Wait for processes and handle shutdown
            self._wait_for_processes(processes)

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nShutting down servers..."))
        finally:
            self._cleanup_processes(processes)

    def _start_frontend_server(self, frontend_dir, port):
        """Start the frontend development server."""
        self.stdout.write(
            self.style.SUCCESS(f"Starting frontend server on port {port}...")
        )

        env = os.environ.copy()
        env["VITE_PORT"] = str(port)

        try:
            process = subprocess.Popen(
                ["npm", "run", "dev:frontend"],
                cwd=frontend_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
            )

            # Start thread to handle frontend output
            threading.Thread(
                target=self._handle_output,
                args=(process, "Frontend"),
                daemon=True,
            ).start()

            return process
        except FileNotFoundError as err:
            raise CommandError(
                "npm not found. Please ensure Node.js and npm are installed."
            ) from err

    def _start_backend_server(self, port):
        """Start the backend development server."""
        self.stdout.write(
            self.style.SUCCESS(f"Starting backend server on port {port}...")
        )

        # Use the current Python executable to ensure we use the same environment
        python_executable = sys.executable

        try:
            process = subprocess.Popen(
                [python_executable, "manage.py", "runserver", f"0.0.0.0:{port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
            )

            # Start thread to handle backend output
            threading.Thread(
                target=self._handle_output,
                args=(process, "Backend"),
                daemon=True,
            ).start()

            return process
        except FileNotFoundError as err:
            raise CommandError("Python not found in PATH.") from err

    def _handle_output(self, process, server_name):
        """Handle output from a subprocess."""
        for line in iter(process.stdout.readline, ""):
            if line.strip():
                prefix = self.style.HTTP_INFO(f"[{server_name}]")
                self.stdout.write(f"{prefix} {line.rstrip()}")

    def _wait_for_processes(self, processes):
        """Wait for all processes to complete or be interrupted."""
        while True:
            # Check if any process has terminated
            for name, process in processes:
                if process.poll() is not None:
                    self.stdout.write(
                        self.style.ERROR(f"{name} server has stopped unexpectedly")
                    )
                    return

            time.sleep(0.5)

    def _cleanup_processes(self, processes):
        """Clean up all running processes."""
        for name, process in processes:
            if process.poll() is None:
                self.stdout.write(self.style.WARNING(f"Terminating {name} server..."))
                try:
                    if sys.platform == "win32":
                        process.terminate()
                    else:
                        process.send_signal(signal.SIGTERM)

                    # Wait for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.stdout.write(
                            self.style.ERROR(f"Force killing {name} server...")
                        )
                        process.kill()
                        process.wait()
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error stopping {name} server: {e}")
                    )
