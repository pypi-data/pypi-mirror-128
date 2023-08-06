import numpy as np

def classification_score(obs, pre, threshold=[0,1,2,3,4,5]):

    r = []
    for i in threshold:
        obs_ = np.where(obs >= i, 1, 0).reshape(-1)
        pre_ = np.where(pre >= i, 1, 0).reshape(-1)
        obs_t, pre_t = 1-obs_, 1-pre_
        
        hits = np.dot(obs_, pre_)
        false_alarms = np.dot(obs_t, pre_)
        misses = np.dot(obs_, pre_t)
        true_positive = np.dot(obs_t,pre_t)

        eps = 0.0001
        ts = hits/(hits+false_alarms+misses+eps)
        tss = (hits/(hits+misses+eps))-(false_alarms/(false_alarms+true_positive+eps))

        num = (hits + false_alarms) * (hits + misses)
        den = hits + misses + false_alarms + true_positive
        Dr = num / den
        ets = (hits - Dr) / (hits + misses + false_alarms - Dr+0.001)
        
        tmp = np.sum(obs_)
        tmp = 1 if tmp<1 else tmp
        bias = np.sum(pre_)/(tmp)
        pod = hits/(hits+misses+eps)

        r.append([ets,tss,pod,bias])
    return np.array(r)
        

if __name__=='__main__':
    from Drawings import mat_bar
    ob = np.array([0,1,2,3,4,5,6,1])
    pr = np.array([0,1,2,2,4,6,6,1])
    m = classification_score(ob,pr)
    import matplotlib.pyplot as plt
    for i in range(4):
        plt.plot(m[:,i])
    plt.legend(['TS','ETS','POD','Bias'])

    plt.figure()
    mat_bar(m.T)
    plt.show()



"""
偏差评分(Bias score)主要用来衡量模式对某一量级降水的预报偏差, 该评分在数值上等于预报区域内满足某降水阈值的总格点数与对应实况降水总格点数的比值。
是用来反映降水总体预报效果的检验方法。
当BIAS>1时, 表示预报结果较实况而言偏湿;
当BIAS < 1时, 表示预报结果较实况而言偏干;
当BIAS=1时, 则表示预报偏差为0, 即预报技巧最高。


由于BIAS评分主要是用于衡量预报区域内满足某降水阈值的预报技巧, 并不能衡量降水的准确率, 因此还需引入公平技巧评分(Equitable Threat Score, ETS)用于衡量对流尺度集合预报的预报效果。
ETS评分表示在预报区域内满足某降水阈值的降水预报结果相对于满足同样降水阈值的随机预报的预报技巧, 因此该评分有效地去除了随机降水概率对评分的影响, 相对而言更加公平、客观。
根据定义, 如果ETS>0时, 表示对于某量级降水来说预报有技巧; 如果ETS≤0时则表示预报没有技巧; 如果ETS=1则表示该预报为完美预报。
"""






















