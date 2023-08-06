import abc


class BaseModel(object):

    model = None
    check_model_weight = ''
    feature_weight_dict = {}

    def __init__(self, X_input, y_input, dict_vec):
        self.train(X_input, y_input)
        self.get_check_model_weight()
        self.get_feature_weight(dict_vec)
        pass

    @abc.abstractmethod
    def train(self, X_input, y_input):
        NotImplemented

    @abc.abstractmethod
    def get_check_model_weight(self):
        NotImplemented

    @abc.abstractmethod
    def get_feature_weight(self, dict_vec):
        NotImplemented

    @abc.abstractmethod
    def score_before_logistic(self, X_input):
        NotImplemented

    @abc.abstractmethod
    def score_label(self, X_input):
        NotImplemented

