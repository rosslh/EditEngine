"""Django management command to build the frontend for production."""

import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style


class Command(BaseCommand):
    help = "Build the frontend for production and collect static files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-static",
            action="store_true",
            help="Skip Django's collectstatic step",
        )
        parser.add_argument(
            "--frontend-only",
            action="store_true",
            help="Only build frontend, skip collectstatic",
        )

    def handle(self, *args, **options):
        self.style = color_style()

        # Get the frontend directory path
        frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"

        if not frontend_dir.exists():
            raise CommandError(f"Frontend directory not found: {frontend_dir}")

        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            raise CommandError(f"package.json not found in {frontend_dir}")

        try:
            # Build the frontend
            self._build_frontend(frontend_dir)

            # Collect static files unless skipped
            if not options["skip_static"] and not options["frontend_only"]:
                self._collect_static()

            self.stdout.write(
                self.style.SUCCESS("✓ Production build completed successfully!")
            )

        except subprocess.CalledProcessError as e:
            raise CommandError(f"Build failed with exit code {e.returncode}") from e
        except Exception as e:
            raise CommandError(f"Build failed: {e}") from e

    def _build_frontend(self, frontend_dir):
        """Build the frontend using npm."""
        self.stdout.write(self.style.SUCCESS("Building frontend for production..."))

        try:
            # Run npm install first to ensure dependencies are up to date
            self.stdout.write("Installing/updating dependencies...")
            subprocess.run(
                ["npm", "install"],
                cwd=frontend_dir,
                check=True,
                capture_output=True,
                text=True,
            )

            # Build the frontend
            self.stdout.write("Building frontend assets...")
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=frontend_dir,
                check=True,
                capture_output=True,
                text=True,
            )

            # Show build output
            if result.stdout:
                self.stdout.write(result.stdout)

            self.stdout.write(self.style.SUCCESS("✓ Frontend build completed"))

        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Frontend build failed: {e.stderr if e.stderr else str(e)}"
                )
            )
            raise
        except FileNotFoundError as err:
            raise CommandError(
                "npm not found. Please ensure Node.js and npm are installed."
            ) from err

    def _collect_static(self):
        """Collect Django static files."""
        self.stdout.write(self.style.SUCCESS("Collecting static files..."))

        try:
            from django.core.management import call_command

            # Run collectstatic with --noinput to avoid prompts
            call_command("collectstatic", "--noinput", verbosity=1)

            self.stdout.write(self.style.SUCCESS("✓ Static files collected"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Static collection failed: {e}"))
            raise CommandError(f"Failed to collect static files: {e}") from e
