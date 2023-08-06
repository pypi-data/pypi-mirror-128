import numpy as np
import pandas as pd

def read_ascii(file,skip=1,dtype=float):
    f = open(file,'r')
    if skip>0:
        f.readlines(skip)
    data = []
    for line in f:
        d = [float(i) for i in line.split(' ') if i not in['','\n']]
        data.append(d)
    return np.array(data)


def maskout(x,y,points,groups=50):
    d = np.array(points)
    num = len(d)
    idx = np.argsort(d[:,0])
    d = d[idx,:]
    
    mask_shape = len(y),len(x)
    mask = np.zeros(mask_shape)
    size = np.round(num/groups)
    groups = np.int(np.ceil(num/size))
    x0 = np.zeros([groups])
    y0 = np.zeros([2,groups])

    for i in range(groups):
        st, ed = int(i*size), int(i*size+size)
        x0[i] = np.mean(d[st:ed,0])
        tmp = np.sort(d[st:ed,1])
        y0[0,i], y0[1,i] = tmp[0], tmp[-1]

    extend_x0 = np.hstack([np.array([x0[0]-0.001]),x0,np.array([x0[-1]+0.001])])
    p=np.argmin(np.abs(x.reshape(-1,1)-extend_x0),axis=1)
    start, end = np.where(p>0)[0][0],np.where(p<groups+1)[0][-1]

    for i in range(start,end+1):
        st = np.where(y>y0[0,p[i]-1])[0][0]
        ed = np.where(y<y0[1,p[i]-1])[0][-1]
        mask[st:ed+1,i] = 1

    mask = mask==0
    return mask

class EOF:
    
    def __init__(self,data):
        
        """
        data : an array with (n,m) shape. m is the space grids while n is the time series grids
        return : an object with EOF analyzing methods
        """
        
        self._shape = data.shape
        self.data = data.reshape(self._shape[0],-1).T


    def fit(self, n_features=3, pre_deal='none', cov_pattern='t'):
        """
        n_features : return some of the features
        pre_deal : the method of data predealing
        'none' means that do not deal with it
        'anomaly' means to caculate the anomaly of the data
        'norm' means to caculte the standarded data

        cov : method of build a covariance matrix
        's' means build a matrix with (m,m) shape
        't' means build a matrix with (n,n) shape
        
        return : return a space function and a time series function. (EOF, PC)
        """
        
        a = self.data - np.mean(self.data,axis=1).reshape(-1,1) if pre_deal != 'none' else self.data
        s = np.sqrt(np.mean(np.power(a,2),axis=1)).reshape(-1,1) if pre_deal == 'norm' else 1
        self.data = a/s
        m, n = self.data.shape

        cov = np.dot(self.data, self.data.T)/n if cov_pattern !='t' else np.dot(self.data.T, self.data)/m

        eig_val, eig_matrix = np.linalg.eig(cov)

        index = np.argsort(eig_val)[::-1]
        self.eig_values, eig_matrix = eig_val[index], eig_matrix[:,index]

        if cov_pattern !='t':
            self.EOF = eig_matrix
            self.PC = np.dot(self.EOF.T, self.data)
        else:
            self.PC = eig_matrix.T
            self.EOF = np.dot(self.data, eig_matrix)

        return self.EOF.T.reshape(self._shape)[:n_features,...], self.PC[:n_features,:]

    def score(self, num=3,decimals=3):
        """
        num : characters of the features
        return : a dataframe of pandas which analyzes the contribution of each feature
        """
        nn = len(self.eig_values) if num==None else int(num)
        self._lamda = self.eig_values
        self._PH = np.round(self._lamda/np.sum(self._lamda),decimals)[:nn]
        self._SPH = np.round([np.sum(self._PH[:i+1]) for i in range(len(self._PH))],decimals)
        self._lamda = self._lamda[:nn]
        m = np.vstack([self._lamda,self._PH,self._SPH]).T
        m[:,0] = np.round(m[:,0],0)
        data = pd.DataFrame(m,index=np.arange(1,nn+1),columns=['lamda','PH','SPH'])
        return data

    def coviarance_contribution(self,n_features=3):
        nn = len(self.eig_values) if n_features==-1 else int(n_features)
        lamda = self.eig_values
        self._PH = lamda[:nn]/np.sum(lamda)
        return self._PH[:nn]

def get_shape(data,origin_scale,new_scale):
    origin_shape = data.shape
    origin_x_right = (origin_shape[1]-1)*origin_scale[0]
    origin_y_down = (origin_shape[0]-1)*origin_scale[1]
    s2, s1 = round(origin_x_right/new_scale[0])+1, round(origin_y_down/new_scale[1])+1
    s2 = s2+1 if s2*new_scale[0]<origin_x_right else s2
    s1 = s1+1 if s2*new_scale[1]<origin_y_down else s1
    return origin_shape,(s1,s2)

def inter(orgin,ref,n,shape):
    new_data = np.zeros(n)
    for i in range(n):
        index = int(i//ref)
        new_index = index if index == shape-1 else index+1
        delta = (i%ref)*(orgin[new_index]-orgin[new_index-1])/ref
        new_data[i] = orgin[index] + delta
    return new_data

def downscale(data,origin_scale,new_scale):
    origin_shape, new_shape = get_shape(data,origin_scale,new_scale)
    new_data = np.zeros(new_shape)
    ref, conti = np.array(origin_scale)/np.array(new_scale), 0
    for j in range(0,new_shape[0]):
        index_origin = int(j//ref[1])
        if (conti==1)|(j%ref[1]==0):
            new_data[j, :], index_new = inter(data[index_origin, :], ref[0], new_shape[1], origin_shape[1]), j
            if index_origin+1<origin_shape[0]:
                gradi = inter(data[index_origin + 1, :], ref[0], new_shape[1], origin_shape[1]) - new_data[j, :]
        if (j%ref[1]+1)<=ref[1]:
            cul = new_data[index_new,:] if conti==0 else inter(data[index_origin, :], ref[0], new_shape[1], origin_shape[1])
            new_data[j,:] = cul + (j%ref[1])*gradi/ref[1]
            conti = 0
        elif (j%ref[1]+1)>ref[1]:
            conti = 1
            new_data[j, :] = new_data[index_new,:] + (j % ref[1]) * gradi/ref[1]
    return new_data

    


if __name__  == '__main__':
    l = np.zeros([80,82])
    print(downscale(l,[0.1,0.1],[0.05,0.05]).shape)
