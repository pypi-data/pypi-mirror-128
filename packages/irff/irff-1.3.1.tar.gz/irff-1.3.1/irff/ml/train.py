from os import popen #,system,
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from .DE import DE
from .ffield import update_ffield
from .evaluate_data import evaluate
from ..data.ColData import ColData
from ..reax import ReaxFF


# getdata = ColData()
# strucs  = ['al4',
#            'c4',
#            'c2al2',
#            'c2f2',
#            'f4',
#            ]

# batchs  = {'others':50}
# dataset = {}

# for mol in strucs:
#     b = batchs[mol] if mol in batchs else batchs['others']
#     trajs = getdata(label=mol,batch=b)
#     dataset.update(trajs)

# reax = ReaxFF(libfile='ffield.json',  
#               dataset=dataset,
#               dft='siesta',
#               # cons=parameters+['val','vale','lp3','cutoff','hbtol'],
#               optword='nocoul',
#               opt=None,
#               batch_size=batch,
#               losFunc='n2',
#               lambda_bd=10000.0,
#               lambda_me=0.01,
#               weight={'others':2.0},
#               convergence=1.0,
#               lossConvergence=0.0) # Loss Functon can be n2,abs,mse,huber
# reax.initialize()
# reax.session(learning_rate=0.0001, method='AdamOptimizer')

def train(step=5000,print_step=100,
             evaluate_step=100,
                      fcsv='ffield.csv',
               to_evaluate=2000,
           lossConvergence=30.0,
               max_ml_iter=100,
            max_generation=100,
                  size_pop=100,
              create_ratio=0.1,
                 potential=None,
                   trainer=None,
                parameters=['boc1','boc2'],
             max_data_size=1000):
    ''' Using machine learing model to assis the training of ReaxFF'''
    sizepop = int(size_pop*(1.0-create_ratio))
    scoreConvergence = - lossConvergence
    
    d = evaluate(model=potential,trainer=trainer,
                 fcsv=fcsv,to_evaluate=to_evaluate,
                 step=evaluate_step,print_step=print_step,
                 evaluate_ffield=True,
                 parameters=parameters)
    d.sort_values(axis=0,by='score',ascending=False,inplace=True)

    X       = d.values[:, : -1]
    Y       = d.values[:, -1]
    columns = d.columns

    ### 训练机器学习模型  ### MLP RF GMM
    ml_model = RandomForestRegressor(n_estimators=100,max_depth=10,oob_score=True).fit(X,Y)
    score    = ml_model.score(X,Y) # cross_val_score(rfr,x,y,cv=10).mean()

    def func(x):                     ## 用于遗传算法评估的函数
        x = np.expand_dims(x,axis=0)
        y = ml_model.predict(x)
        return -np.squeeze(y)

    if d.shape[0]>sizepop:
       # d_ = d.sample(n=sizepop, replace=False, weights=None, random_state=1, axis=0)
       d_ = d[:sizepop]
    else:
       d_ = d

    it_     = 0
    score   = scoreConvergence - 1.0
    while score<scoreConvergence and it_< max_ml_iter:
        # d   = evaluate(model=potential,trainer=trainer,fcsv=fcsv,
        #                to_evaluate=to_evaluate, # Y[-1]+0.0001,
        #                step=evaluate_step,print_step=print_step,
        #                parameters=parameters)
        X   = d.values[:, : -1]
        Y   = d.values[:, -1]
        ml_model.fit(X,Y)
        score_ = ml_model.score(X,Y) # cross_val_score(rfr,x,y,cv=10).mean()
        print('The accuraccy of the mathine learning model: {:f}'.format(score_))

        nrow = d_.shape[0]
        if nrow>sizepop:
           d_.drop(nrow-1,axis=0,inplace=True) 
        nrow = d.shape[0]
        if nrow>max_data_size:
           d.drop(nrow-1,axis=0,inplace=True) 
        X_ = d_.values[:, : -1]

        ## if PSO DE GMM
        print('Do genetic evolute ...')

        lb=0.9*np.min(X_,axis=0)
        ub=1.1*np.max(X_,axis=0)
        de = DE(func,n_dim=X_.shape[1], F=0.5,size_pop=100,
                max_iter=max_generation, 
                prob_mut=0.1,lb=lb, 
                ub=ub,X_input=X_)             
        best_x,best_y=de.run()                     ###   PSO GMM
        print('The guessed score of best candidate: {:f}'.format(float(best_y)))

        new_row = {}
        for i,key in enumerate(columns):
            if key != 'score':
               new_row[key] = best_x[i]

        if not potential is None:                  #### 两种引入方式 potential or trainer
           potential.update(p=new_row)
           potential.run(learning_rate=1.0e-4,step=step,print_step=print_step,
                          writelib=1000,close_session=False)
           p_      = potential.p_ 
           score   = -potential.loss_
        elif not trainer is None:
           update_ffield(new_row,'ffield.json')    #### update parameters
           loss,p_ = trainer(step=step,print_step=print_step)
           score   = -loss
        else:
           raise RuntimeError('-  At least one of potential or trainer function is defind!')

        if score>d.loc[0, 'score']:
           popen('cp ffield.json ffield_best.json')

        if score>-9999999.0:
           for i,key in enumerate(columns):
               if key != 'score':
                  new_row[key] = p_[key]        
        new_row['score'] = score 
       
        d = d.append(new_row,ignore_index=True)
        print('The score after gradient descent: {:f}'.format(score))
        d.sort_values(axis=0,by='score',ascending=False,inplace=True)
        d_ = d_.append(new_row,ignore_index=True)
        d_.sort_values(axis=0,by='score',ascending=False,inplace=True)

        print('Saving the data to {:s} ...'.format(fcsv))
        d.to_csv(fcsv)
        it_ += 1

