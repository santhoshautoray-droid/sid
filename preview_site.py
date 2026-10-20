"""Local-only static preview: serve the built site, never the source checkout."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent / "dist"


class PreviewHandler(SimpleHTTPRequestHandler):
    server_version = "StaticPreview"
    sys_version = ""

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_head(self):
        path = unquote(urlsplit(self.path).path)
        target = Path(self.translate_path(self.path)).resolve()
        if (not target.is_relative_to(ROOT.resolve())
                or any(part.startswith(".") for part in Path(path).parts)
                or target.name == "_headers"):
            self.send_error(404)
            return None
        return super().send_head()

    def end_headers(self):
        for line in (ROOT / "_headers").read_text(encoding="utf-8").splitlines():
            if line.startswith("  ") and ": " in line:
                name, value = line.strip().split(": ", 1)
                # HSTS belongs on the HTTPS production response only.
                if name != "Strict-Transport-Security":
                    self.send_header(name, value)
        super().end_headers()


if __name__ == "__main__":
    if not (ROOT / "index.html").is_file():
        raise SystemExit("Build the site before starting its preview.")
    port = int(os.environ.get("SIDDHA_PREVIEW_PORT", "8790"))
    print(f"Local preview: http://127.0.0.1:{port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), partial(PreviewHandler, directory=str(ROOT))).serve_forever()
