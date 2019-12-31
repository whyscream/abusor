from django.core.management.base import BaseCommand
from django.db import transaction

from abusor.events.models import Case
from abusor.rules.models import CaseRule
from abusor.rules.processing import apply_rules


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
            with transaction.atomic():
                case.recalculate_score()
                case, num_applied = apply_rules(case, CaseRule.objects.all())
                case.save()
                if num_applied:
                    if case.end_date:
                        closed_cases += 1
                        msg = f"Case {case} updated by {num_applied} rules and closed."
                    else:
                        updated_cases += 1
                        msg = "Case {case} updated by {num_applied} rules."
                    self.stdout.write(msg)

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed {cases.count()} cases, updated {updated_cases} "
                f"and closed {closed_cases}."
            )
        )
