# books_uuid_extractor.py
import posixpath
from pathlib import Path
from pymobiledevice3.services.os_trace import OsTraceService
from pymobiledevice3.services.dvt.instruments.process_control import ProcessControl


class BooksUUIDExtractor:
    def __init__(self, lockdown_client, dvt_service):
        self.lockdown = lockdown_client
        self.dvt = dvt_service
        self.uuid_file = Path("uuid.txt")

    def extract(self):
        # Use cached UUID if valid
        if self.uuid_file.exists():
            uuid = self.uuid_file.read_text().strip()
            if len(uuid) > 10:
                return uuid

        # Launch Books app
        ProcessControl(self.dvt).launch("com.apple.iBooks")

        # Scan syslog for bookassetd UUID
        for entry in OsTraceService(lockdown=self.lockdown).syslog():
            if posixpath.basename(entry.filename) != "bookassetd":
                continue
            if "/Documents/BLDownloads/" not in entry.message:
                continue

            # Extract UUID safely
            try:
                uuid = entry.message.split("/SystemGroup/")[1].split("/Documents")[0]
            except Exception:
                continue

            self.uuid_file.write_text(uuid)
            return uuid

        return None
