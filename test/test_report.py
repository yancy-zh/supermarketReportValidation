from unittest import TestCase

from report import Report


class TestReport(TestCase):
    report = Report("", "", "")

    def test_rate_to_decimal(self):
        decimal = self.report.rateToDecimal(rate="16.00%")
        self.assertEqual(decimal, 0.16)
