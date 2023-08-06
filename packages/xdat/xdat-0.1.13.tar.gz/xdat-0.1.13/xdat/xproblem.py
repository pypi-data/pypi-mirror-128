import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.base import clone
from . import xutils


def cv_split(df, n_splits=12, group_on=None):
    df = df.sample(frac=1.).reset_index(drop=True)
    groups = df[group_on] if group_on else None

    if group_on is None:
        if n_splits == 'max':
            n_splits = len(df)

        kfold = model_selection.KFold(n_splits=n_splits)

    else:
        num_groups = len(np.unique(groups))
        if n_splits == 'max':
            n_splits = num_groups

        n_splits = min(n_splits, num_groups)
        kfold = model_selection.GroupKFold(n_splits=n_splits)

    for train_index, test_index in kfold.split(df, groups=groups):
        df_train = df.iloc[train_index].reset_index(drop=True)
        df_test = df.iloc[test_index].reset_index(drop=True)
        yield df_train, df_test


def train_cv(df, target_col, clf, n_splits=12, group_on=None, ordered_split=False, del_cols=tuple(), uid_col=None):
    all_folds = []
    fold_num = 1
    for df_train, df_test in cv_split(df, n_splits=n_splits, group_on=group_on):
        clf_fold = clone(clf)
        test_tmp_uid = df_test[uid_col] if uid_col else None

        if ordered_split and group_on:
            assert n_splits == 'max'
            test_group = df_test[group_on].min()
            df_train = df_train[df_train[group_on] < test_group].reset_index(drop=True)
            assert (df_train[group_on] >= test_group).sum() == 0
            if len(df_train) == 0:
                continue

        if del_cols:
            df_train.drop(columns=del_cols, errors='ignore', inplace=True)
            df_test.drop(columns=del_cols, errors='ignore', inplace=True)

        # offs = df_train.groupby('p').mean()[['target']].reset_index()
        # offs.columns = ['p', 'offset']
        # print(offs)
        # df_test = df_test.merge(offs, how = 'left', on=['p'])
        # df_test['offset'] = df_test['offset'].fillna(df_train['target'].mean())
        X_train, y_train = xutils.split_X_y(df_train, target_col)
        clf_fold.fit(X_train, y_train)
        #print(clf_fold[2].coef_)
        X_test, y_test = xutils.split_X_y(df_test, target_col)
        pred = clf_fold.predict(X_test)
        df_test['pred'] = pred
        df_test['fold_num'] = fold_num
        if uid_col:
            df_test[uid_col] = test_tmp_uid
        all_folds.append([clf_fold, df_train, df_test])
        fold_num += 1

    df_test = pd.concat([i[2] for i in all_folds], ignore_index=True)
    df_test = df_test.reset_index(drop=True)
    return df_test, all_folds


def eval_test(df_test, eval_per=None, metrics=None):
    df_test = df_test.copy()
    df_test['none'] = 'none'

    if not isinstance(eval_per, list) and not isinstance(eval_per, tuple):
        eval_per = [eval_per]

    rows = []
    for curr_group in eval_per:
        if not curr_group:
            curr_group = 'none'

        for gval in df_test[curr_group].unique():
            df_g = df_test[df_test[curr_group] == gval]
            row = {n: f(df_g.target, df_g.pred) for n, f in metrics.items()}
            row['cv_grouping'] = curr_group
            row['cv_group_key'] = str(gval)
            row['cv_group_size'] = len(df_g)
            rows.append(row)

    df_res = pd.DataFrame(rows)
    return df_res