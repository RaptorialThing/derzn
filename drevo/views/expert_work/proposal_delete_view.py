from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from drevo.models import InterviewAnswerExpertProposal


class ProposalDeleteView(DeleteView):
    """
    Удаляет мнение эксперта по ответу на вопрос интервью
    """

    model = InterviewAnswerExpertProposal
    success_url = reverse_lazy("/drevo/")
#    def get_success_url(self):
#        return self.request.META.get('HTTP_REFERER')
