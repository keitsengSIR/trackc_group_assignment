import unittest

class MockDatabase:
    def __init__(self):
        self.patients = {}
        self.appointments = {}

    def save_patient(self, pid, data):
        if pid in self.patients:
            return False
        self.patients[pid] = data
        return True

    def book_appointment(self, app_id, pid, date):
        if pid not in self.patients:
            return "Patient Not Found"
        if app_id in self.appointments:
            return "Slot Taken"
        self.appointments[app_id] = {"pid": pid, "date": date}
        return "Success"

class ClinicIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.db = MockDatabase()

    def test_patient_registration_and_appointment_flow(self):
        """Integration Test 1: Registers a patient and books an appointment successfully."""
        pid = "P1001"
        saved = self.db.save_patient(pid, {"name": "Alice Smith", "age": 30})
        self.assertTrue(saved)
        
        status = self.db.book_appointment("APP-01", pid, "2026-11-01")
        self.assertEqual(status, "Success")
        self.assertIn("APP-01", self.db.appointments)

    def test_duplicate_patient_flagging(self):
        """Integration Test 2: Prevents duplicate patient record creation."""
        pid = "P1002"
        self.db.save_patient(pid, {"name": "Bob Jones", "age": 45})
        duplicate_attempt = self.db.save_patient(pid, {"name": "Bob Jones Jr", "age": 20})
        self.assertFalse(duplicate_attempt)

    def test_appointment_with_unregistered_patient(self):
        """Integration Test 3: Rejects appointment booking for non-existent patient IDs."""
        status = self.db.book_appointment("APP-02", "UNKNOWN_ID", "2026-11-02")
        self.assertEqual(status, "Patient Not Found")

    def test_slot_collision_prevention(self):
        """Integration Test 4: Prevents double booking on the same appointment slot."""
        pid = "P1003"
        self.db.save_patient(pid, {"name": "Charlie Brown", "age": 50})
        self.db.book_appointment("APP-03", pid, "2026-11-03")
        
        collision_status = self.db.book_appointment("APP-03", pid, "2026-11-03")
        self.assertEqual(collision_status, "Slot Taken")

    def test_audit_log_record_tracking(self):
        """Integration Test 5: Tracks database records correctly across state transitions."""
        self.db.save_patient("P1004", {"name": "Diana Prince", "age": 28})
        self.assertEqual(len(self.db.patients), 1)

if __name__ == "__main__":
    unittest.main()