"""
High-Performance Python 3.14 Web Server & REST API Backend for Bhoomi-AI.
Serves static frontend SPA files and provides full REST endpoints for OCR, NER,
Validation Rule Engine, Cadastral GIS, Active Learning, and Audit Tracking.
"""

import os
import sys
import json
import uuid
import socket
import datetime
import mimetypes
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# Import backend modules
from database import db, SCOPE_OF_STUDY_DATA
from ocr_engine import ocr_engine
from validation_engine import validation_engine
from active_learning import ActiveLearningEngine
from cadastral_gis import CadastralGISEngine

active_learning_engine = ActiveLearningEngine(db)
cadastral_engine = CadastralGISEngine(db)

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

class LandRecordAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean background logging
        pass

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def _send_json(self, data, status_code=200):
        response_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/code.html':
            try:
                filename = 'code.html' if os.path.exists('code.html') else 'index.html'
                with open(filename, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, f"Error loading page: {e}")
                return
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path
                query = urllib.parse.parse_qs(parsed.query)
    
            # -----------------------------------------------------------------
            # API Endpoints
            # -----------------------------------------------------------------
                if path.startswith("/api/"):
                    if path == "/api/kpis":
                        stats = db.get_kpis()
                        self._send_json({"success": True, "data": stats})
                        return
    
                    elif path == "/api/records":
                        q = query.get("q", [None])[0]
                        state = query.get("state", [None])[0]
                        status = query.get("status", [None])[0]
                        district = query.get("district", [None])[0]
                        records = db.search_records(query=q, state=state, status=status, district=district)
                        self._send_json({"success": True, "count": len(records), "data": records})
                        return
    
                    elif path.startswith("/api/records/"):
                        record_id = path.replace("/api/records/", "").strip()
                        record = db.get_record_by_id(record_id)
                        if record:
                            boxes = ocr_engine.generate_bounding_boxes(record)
                            val_res = validation_engine.validate_record(record, db.get_all_records())
                            self._send_json({
                                "success": True,
                                "data": record,
                                "boundingBoxes": boxes,
                                "validation": val_res
                            })
                        else:
                            self._send_json({"success": False, "error": "Record not found"}, 404)
                        return
    
                    elif path == "/api/cadastral/geojson":
                        geojson = cadastral_engine.get_all_parcels()
                        self._send_json({"success": True, "data": geojson})
                        return
    
                    elif path.startswith("/api/cadastral/parcel/"):
                        parcel_id = path.replace("/api/cadastral/parcel/", "").strip()
                        parcel = cadastral_engine.get_parcel_by_id(parcel_id)
                        if parcel:
                            self._send_json({"success": True, "data": parcel})
                        else:
                            self._send_json({"success": False, "error": "Parcel not found"}, 404)
                        return
    
                    elif path == "/api/active-learning/metrics":
                        data = active_learning_engine.get_metrics()
                        self._send_json({"success": True, "data": data})
                        return
    
                    elif path == "/api/audit/logs":
                        logs = db.get_audit_logs(60)
                        self._send_json({"success": True, "count": len(logs), "data": logs})
                        return
    
                    elif path == "/api/scope-of-study":
                        self._send_json({"success": True, "data": SCOPE_OF_STUDY_DATA})
                        return
    
                    else:
                        self._send_json({"success": False, "error": "Unknown API endpoint"}, 404)
                        return

        # -----------------------------------------------------------------
        # Static Frontend File Serving
        # -----------------------------------------------------------------
        req_path = path.lstrip("/")
        if not req_path or req_path == "index.html":
            file_path = os.path.join(FRONTEND_DIR, "index.html")
        else:
            file_path = os.path.join(FRONTEND_DIR, req_path)

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            file_path = os.path.join(FRONTEND_DIR, "index.html")

        if os.path.exists(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                if file_path.endswith(".js"):
                    mime_type = "application/javascript"
                elif file_path.endswith(".css"):
                    mime_type = "text/css"
                elif file_path.endswith(".json"):
                    mime_type = "application/json"
                elif file_path.endswith(".svg"):
                    mime_type = "image/svg+xml"
                else:
                    mime_type = "text/html"

            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "javascript" in mime_type else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        if path == "/api/documents/process-ocr" or path == "/api/documents/upload":
            filename = body.get("filename", "scanned_doc.png")
            raw_text = body.get("rawText", None)
            state_hint = body.get("stateCode", "UP")

            # Ingest and perform multilingual OCR & entity classification
            new_record = ocr_engine.process_raw_document(filename, raw_text, state_hint)
            
            # Apply 6-tier validation
            val_res = validation_engine.validate_record(new_record, db.get_all_records())
            new_record["status"] = "Validated" if val_res["isValid"] and new_record["confidenceScores"]["overall"] >= 90 else "Review Required"
            
            # Save into DB
            saved = db.add_record(new_record)
            
            # Generate Cadastral polygon
            cadastral_engine.add_or_update_parcel(saved)
            
            boxes = ocr_engine.generate_bounding_boxes(saved)

            self._send_json({
                "success": True,
                "message": "Document successfully processed and categorized.",
                "data": saved,
                "boundingBoxes": boxes,
                "validation": val_res
            })
            return

        elif path == "/api/records/update":
            record_id = body.get("recordId")
            fields = body.get("fields", {})
            user = body.get("user", "tehsildar_user")
            role = body.get("role", "Tehsildar")

            if not record_id:
                self._send_json({"success": False, "error": "recordId is required"}, 400)
                return

            updated = db.update_record(record_id, fields, user=user, role=role)
            if updated:
                # Re-validate
                val_res = validation_engine.validate_record(updated, db.get_all_records())
                cadastral_engine.add_or_update_parcel(updated)
                self._send_json({
                    "success": True,
                    "message": "Record successfully updated and audit logged.",
                    "data": updated,
                    "validation": val_res
                })
            else:
                self._send_json({"success": False, "error": "Record not found"}, 404)
            return

        elif path == "/api/validation/run-rules":
            record = body.get("record")
            if not record:
                self._send_json({"success": False, "error": "record object required"}, 400)
                return
            res = validation_engine.validate_record(record, db.get_all_records())
            self._send_json({"success": True, "validation": res})
            return

        elif path == "/api/active-learning/retrain":
            cycle_result = active_learning_engine.trigger_retraining_cycle()
            db.log_audit(
                user=body.get("user", "nodal_admin"),
                role="Admin",
                action="ACTIVE_LEARNING_RETRAIN",
                record_id="MODEL_GLOBAL",
                details=f"Triggered retrain cycle. New model: {cycle_result['modelVersion']}"
            )
            self._send_json({"success": True, "data": cycle_result})
            return

        elif path == "/api/certificate/generate":
            record_id = body.get("recordId")
            record = db.get_record_by_id(record_id)
            if not record:
                self._send_json({"success": False, "error": "Record not found"}, 404)
                return

            cert_payload = {
                "certificateId": f"ROR-CERT-{uuid.uuid4().hex[:10].upper()}",
                "recordId": record["id"],
                "landowner": record.get("landownerName"),
                "khasra": record.get("khasraNo"),
                "khata": record.get("khataNo"),
                "village": record.get("village"),
                "district": record.get("district"),
                "state": record.get("state"),
                "area": record.get("totalArea"),
                "issuedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "issuer": "Revenue Department & DILRMP National Node",
                "sha256Hash": f"SHA256:{uuid.uuid4().hex}{uuid.uuid4().hex[:16]}",
                "verificationUrl": f"https://landrecords.gov.in/verify?rec={record['id']}&auth=gov_dilrmp"
            }

            db.log_audit(
                user=body.get("user", "citizen_portal"),
                role="Citizen/Public",
                action="GENERATE_CERTIFIED_ROR",
                record_id=record["id"],
                details=f"Generated Certified RoR with Cert ID {cert_payload['certificateId']}"
            )

            self._send_json({"success": True, "data": cert_payload})
            return

        else:
            self._send_json({"success": False, "error": "Unknown POST endpoint"}, 404)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_available_port(start_port=8000, max_attempts=50):
    for p in range(start_port, start_port + max_attempts):
        if not is_port_in_use(p):
            return p
    return start_port

def run_server(port=None):
    if port is None or is_port_in_use(port):
        port = find_available_port(start_port=8000)

    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, LandRecordAPIHandler)
    print(f"=======================================================================")
    print(f"  BHOOMIDRISHTI AI (DILRMP Modernization Platform)")
    print(f"  Server listening on:")
    print(f"  --> http://localhost:{port}")
    print(f"  --> http://127.0.0.1:{port}")
    print(f"  Multi-threaded REST endpoints ready.")
    print(f"=======================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_server(port)
