from libya_tally.apps.tally.models.result_form import ResultForm
from libya_tally.libs.models.enums.form_state import FormState
from libya_tally.libs.tests.test_base import create_result_form, TestBase
from libya_tally.libs.reports import progress


class TestArchive(TestBase):
    def setUp(self):
        create_result_form(
            barcode=1, serial_number=1, form_state=FormState.UNSUBMITTED)
        create_result_form(
            barcode=2, serial_number=2, form_state=FormState.INTAKE)
        create_result_form(
            barcode=3, serial_number=3, form_state=FormState.CLEARANCE)
        create_result_form(
            barcode=4, serial_number=4, form_state=FormState.DATA_ENTRY_1)
        create_result_form(
            barcode=5, serial_number=5, form_state=FormState.DATA_ENTRY_2)
        create_result_form(
            barcode=6, serial_number=6, form_state=FormState.CORRECTION)
        create_result_form(
            barcode=7, serial_number=7, form_state=FormState.QUALITY_CONTROL)
        create_result_form(
            barcode=8, serial_number=8, form_state=FormState.AUDIT)
        create_result_form(
            barcode=9, serial_number=9, form_state=FormState.UNSUBMITTED)
        create_result_form(
            barcode=10, serial_number=10, form_state=FormState.ARCHIVING)
        create_result_form(form_state=FormState.ARCHIVING)
        self.assertEqual(ResultForm.objects.count(), 11)

    def test_expected_progress_report(self):
        report = progress.ExpectedProgressReport()
        self.assertEqual(report.number, 11)
        self.assertEqual(report.total, 11)
        self.assertEqual(report.percentage, 100.0)
