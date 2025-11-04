# verification.py
import hashlib
import time
import json

def compute_hash(file_bytes):
    h = hashlib.sha256()
    h.update(file_bytes)
    return h.hexdigest()

def create_proof_record(filename, file_hash):
    record = {
        "filename": filename,
        "hash": file_hash,
        "timestamp": int(time.time())
    }
    return record

def store_proof_local(record, ledger_path="ledger.json"):
    try:
        with open(ledger_path, "r") as f:
            ledger = json.load(f)
    except FileNotFoundError:
        ledger = []
    ledger.append(record)
    with open(ledger_path, "w") as f:
        json.dump(ledger, f, indent=2)
    return True
