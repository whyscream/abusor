from django.core.management.base import BaseCommand

from abusor.events.models import Case


class Command(BaseCommand):
    help = "Recalculate case scores."

    def handle(self, *args, **kwargs):
        """Recalculte open case scores, and apply business rules to them."""
        cases = Case.objects.filter(end_date=None)
        if not cases:
            self.stdout.write(self.style.SUCCESS("No open cases found."))
            return

        updated_cases = 0
        closed_cases = 0
        for case in cases:
            applied = case.apply_business_rules()  # also recalculates scores
            if applied:
                if case.end_date:
                    closed_cases += 1
                    msg = "Case '{}' updated by {} rule(s) and closed."
                else:
                    updated_cases += 1
                    msg = "Case '{}' updated by {} rule(s)."
                self.stdout.write(msg.format(case, applied))

        self.stdout.write(
            self.style.SUCCESS(
                "Processed {} cases, updated {} and closed {}.".format(
                    cases.count(), updated_cases, closed_cases
                )
            )
        )
