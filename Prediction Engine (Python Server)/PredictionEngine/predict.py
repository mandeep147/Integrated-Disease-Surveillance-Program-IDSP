
#print result.summary()

#print result.conf_int()


#print np.exp(result.params)

#params = result.params
#conf = result.conf_int()
#conf['OR'] = params
#conf.columns = ['2.5%', '97.5%', 'OR']
#print np.exp(conf)

#print result.predict([48,1,0])

def predictResult(location, disease, ycases):
	import pandas as pd
	import numpy as np
	import statsmodels.api as sm
	#from sklearn import tree

	df = pd.read_csv("traindata.csv") 
	train_cols = ['location','disease','ycases']
	logit = sm.Logit(df['cases'], df[train_cols])
	result = logit.fit()
	finalresult = result.predict([location, disease, ycases])
	return finalresult
