from rest_framework.throttling import UserRateThrottle


class QuestionThrottle(UserRateThrottle):
    scope = 'question'

    def allow_request(self, request, view):

        if request.method == 'GET':
            return True
        
        if 'question-' + request.method.lower() in self.THROTTLE_RATES:
            self.scope = 'question-' + request.method.lower()

        return super().allow_request(request, view)