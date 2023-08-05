import arrow
from typing import List

from cached_property import cached_property

from canvas_workflow_kit import events
from canvas_workflow_kit.protocol import ClinicalQualityMeasure, ProtocolResult, STATUS_DUE, STATUS_SATISFIED
from canvas_workflow_kit.recommendation import Recommendation
from canvas_workflow_kit.value_set.v2020 import DiagnosisOfHypertension


class Ccp003v1(ClinicalQualityMeasure):
    title = 'Diagnosis Of Hypertension'

    description = 'All patients with Diagnosis Of Hypertension.'
    information = 'https://canvas-medical.zendesk.com/hc/en-us'

    identifiers = ['CCP003v1']

    types = ['CCP']

    responds_to_event_types = [
        events.HEALTH_MAINTENANCE,
    ]
    authors = [
        'Canvas Medical Team',
    ]

    @property
    def references(self) -> List[str]:
        return ['Canvas Medical CCP, https://canvas-medical.zendesk.com/hc/en-us']

    funding_source = ''

    compute_on_change_types = [
        ClinicalQualityMeasure.CHANGE_CONDITION,
    ]

    @classmethod
    def revision(cls) -> str:
        return '2020-04-02v1'

    @cached_property
    def date_of_diagnosis(self) -> str:
        actives: List = []
        for item in self.patient.conditions.find(DiagnosisOfHypertension):
            actives.extend([period['from'] for period in item['periods'] if period['to'] is None])
        return min(actives) if actives else ''

    def in_initial_population(self) -> bool:
        """
        All patients
        """
        return True

    def in_denominator(self) -> bool:
        """
        Patients in the initial population
        """
        return self.in_initial_population()

    def in_numerator(self) -> bool:
        """
        Patients that have been diagnosed with hypertension
        """
        return bool(self.date_of_diagnosis)

    def compute_results(self) -> ProtocolResult:
        result = ProtocolResult()
        if self.in_denominator():
            if self.in_numerator():
                result.due_in = 0
                result.status = STATUS_DUE
                date = arrow.get(self.date_of_diagnosis).format('ddd, MMM Do YYYY')
                narrative = (f'{self.patient.first_name} has been diagnosed '
                             f'of hypertension on {date}.')
                result.add_narrative(narrative)
                result.add_recommendation(
                    Recommendation(
                        key='CCP003v1_RECOMMEND_CONTACT',
                        rank=1,
                        button='Communication',
                        title='Contact the patient',
                        narrative=narrative,
                        command={'key': 'schedule'}))
            else:
                result.due_in = -1
                result.status = STATUS_SATISFIED
                narrative = f'{self.patient.first_name} has not been diagnosed of hypertension.'
                result.add_narrative(narrative)

        return result
