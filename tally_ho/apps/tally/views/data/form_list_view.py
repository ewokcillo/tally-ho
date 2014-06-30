from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from djqscsv import render_to_csv_response
from eztables.views import DatatablesView
from guardian.mixins import LoginRequiredMixin

from tally_ho.apps.tally.models.ballot import Ballot
from tally_ho.apps.tally.models.result_form import ResultForm
from tally_ho.libs.models.enums.form_state import FormState
from tally_ho.libs.permissions import groups
from tally_ho.libs.views import mixins


ALL = '__all__'


class FormListDataView(LoginRequiredMixin,
                       mixins.GroupRequiredMixin,
                       mixins.DatatablesDisplayFieldsMixin,
                       DatatablesView):
    group_required = groups.SUPER_ADMINISTRATOR
    model = ResultForm
    fields = (
        'barcode',
        'center__code',
        'station_number',
        'center__office__name',
        'center__office__number',
        'ballot__number',
        'ballot__race_type',
        'form_state',
        'modified_date',
    )
    display_fields = (
        ('barcode', 'barcode'),
        ('center__code', 'center_code'),
        ('station_number', 'station_number'),
        ('center__office__name', 'center_office'),
        ('center__office__number', 'center_office_number'),
        ('ballot__number', 'ballot_number'),
        ('ballot__race_type', 'ballot_race_type_name'),
        ('form_state', 'form_state_name'),
        ('modified_date', 'modified_date_formatted'),
    )

    def get_queryset(self):
        qs = super(FormListDataView, self).get_queryset()
        ballot_number = self.kwargs.get('ballot')

        if ballot_number:
            ballot = Ballot.objects.get(number=ballot_number)
            qs = qs.filter(
                ballot__number__in=ballot.form_ballot_numbers)

        return qs


class FormListView(LoginRequiredMixin,
                   mixins.GroupRequiredMixin,
                   TemplateView):
    group_required = groups.SUPER_ADMINISTRATOR
    template_name = "data/forms.html"

    def get(self, *args, **kwargs):
        form_state = kwargs.get('state')

        if form_state:
            if form_state == ALL:
                form_list = ResultForm.objects.all()
            else:
                form_state = FormState.get(form_state)
                form_list = ResultForm.forms_in_state(form_state.value)

            form_list = form_list.values(
                'barcode', 'form_state', 'gender', 'station_number',
                'center__sub_constituency__code',
                'center__code',
                'ballot__race_type').order_by('barcode')

            return render_to_csv_response(form_list)

        return self.render_to_response(
            self.get_context_data(header_text=_('Form List'),
                                  remote_url='form-list-data'))


class FormNotReceivedListView(FormListView):
    group_required = groups.SUPER_ADMINISTRATOR

    def get(self, *args, **kwargs):
        format_ = kwargs.get('format')
        if format_ == 'csv':
            form_list = ResultForm.forms_in_state(FormState.UNSUBMITTED).\
                values('id',
                       'created_date',
                       'modified_date',
                       'ballot_id__number',
                       'center_id__code',
                       'user_id__username',
                       'created_user_id__username',
                       'audited_count',
                       'barcode',
                       'date_seen',
                       'form_stamped',
                       'form_state',
                       'gender',
                       'name',
                       'office_id__number',
                       'rejected_count',
                       'serial_number',
                       'skip_quarantine_checks',
                       'station_number',
                       'is_replacement',
                       'intake_printed',
                       'clearance_printed')
            return render_to_csv_response(form_list)

        return self.render_to_response(
            self.get_context_data(header_text=_('Forms Not Received'),
                                  custom=True,
                                  remote_url='form-not-received-data'))


class FormNotReceivedDataView(FormListDataView):
    queryset = ResultForm.forms_in_state(FormState.UNSUBMITTED)


class FormsForRaceView(FormListView):
    group_require = groups.SUPER_ADMINISTRATOR

    def get(self, *args, **kwargs):
        ballot = kwargs.get('ballot')

        return self.render_to_response(self.get_context_data(
            header_text=_('Forms for Race %s' % ballot),
            none=True,
            remote_url='/data/forms-for-race-data/%s/' % ballot))
