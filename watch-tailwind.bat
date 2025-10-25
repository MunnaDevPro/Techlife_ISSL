@echo off
echo Starting Tailwind CSS watcher...
echo Press Ctrl+C to stop
npx @tailwindcss/cli -i input.css -o static/css/output.css --watch