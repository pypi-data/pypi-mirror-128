# -*- coding: utf-8 -*-
from abc import ABC
from .base_model import BaseModel
import numpy as np
from sklearn.linear_model import LogisticRegressionCV


class CvLrModel(BaseModel, ABC):

    def train(self, X_train, y_train):
        clf = LogisticRegressionCV(
            Cs=[.02, .04, .06, .08, .1, .2, .4, .6, .8, 1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100],
            cv=2, scoring='roc_auc', random_state=0, penalty='l1', solver='liblinear', refit=True)

        if X_train is None or X_train is None or len(X_train) != len(X_train):
            raise Exception('X_train is None or y_train is None or len(X_train) != len(y_train)')
        clf.fit(X_train, y_train)
        # 打印记录
        print(f'CvLrModel clf.scores_:\n {clf.scores_}')
        print(f'CvLrModel clf.C_: {clf.C_}')
        print(f'CvLrModel feature_importances_weight: {clf.coef_}')
        self.model = clf
        return self.model

    def get_check_model_weight(self):
        self.model.sparsify()
        self.check_model_weight = f'check_parameter:\nclf.C_: {self.model.C_}\nfeature_importances_weight: \n{self.model.coef_}'
        self.model.densify()
        return self.check_model_weight

    def get_feature_weight(self, dict_vec):
        feature_name_list = dict_vec.get_feature_names()
        feature_weight_list = self.model.coef_
        for name, weight in np.array([feature_name_list, feature_weight_list[0]]).T:
            self.feature_weight_dict[name] = weight
        return self.feature_weight_dict

    def score_before_logistic(self, X_input):
        return self.model.decision_function(X_input)

    def score_label(self, X_input):
        return self.model.predict(X_input)
