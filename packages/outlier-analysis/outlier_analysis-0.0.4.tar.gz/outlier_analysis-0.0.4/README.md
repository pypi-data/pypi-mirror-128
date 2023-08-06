# Package Documentation

### Instalation
```python
pip install outlier_analysis

import outlier_analysis as oa
```

### Packge Design
The package will be a batch processing software that allows the user to clean up their data without having to know about pipelines or outlier detection methods. The package will consist of 3 layers, the first layer will use Standard Deviation to set a dynamic max, next will be DBSCAN, then Local Outlier Detection. 

#### Helpful links to understand the methodology behind the package
https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html

https://medium.com/learningdatascience/anomaly-detection-techniques-in-python-50f650c75aaf

https://www.youtube.com/watch?v=SawQZdAcazY

https://towardsdatascience.com/pipelines-custom-transformers-in-scikit-learn-the-step-by-step-guide-with-python-code-4a7d9b068156

https://www.youtube.com/watch?v=HdlDYng8g9s

#### Standard Deviation
Standard deviation will be anything within 3 deviations. We use this to get rid of any extreme outliers that may be hidden within the data. 

They will also be able to retrieve the model parameters through outlier_detection.stdev.return_model_.
#### DBSCAN
This method will have a default value of .35 for the eps parameter, which is essentially the distance between points. Metric will be Euclidean distance with min_samples set to a default of 10. 

The user will able be able to customize the model by setting dbscan_param to a dictionary of the parameters. They will also be able to get the values they used in the model and return the actual model itself. 
#### Local Outlier Factor (LOF)
This method will have a default number of neighbors as 1, using a manhattan distance as the metric. 

The user will be able to customize the model by setting lof_params as a dictionary with all of the parameters. To get the parameters, call outlier_detection_drl.get_params().
#### Design
The structure for the package will be as follows:
- Start with taking the data as a whole and passing it through the Standard Deviation model to trim off any extreme values that don't belong in the range of the data
- Take the output of the previous model then split it up based on a categorical value (optional).
- Take each individual categorical value and run it through its own fit_predict function and have each grouping remove the outliers and return the clean set. 
- Take the return data from the DBSCAN model and pass it through its own Local Outlier Factor model then return the data.
- Take the return data then concat the individual dataframes together to return the data as a whole. 


#### Use Cases
##### Basic Outlier Use Cases
- User is able to pass in the whole dataframe, the column they wish to scan for outliers and have it run through standard deviation, DBSCAN and Local Outlier Factor functions for a clean dataset.
- User is able to do everything as defined in the steps above, but they can also pass in a group by column if they wish to scan for outliers based on different hierarchys
- User is able to do everything as defined in the steps above, but they can also pass in custom parameters for the DBSCAN and LOF methods
##### Custom Model and Model Return Use Cases
- User is able to return the model itself (as long as there is no group_column) in the case of DBSCAN and LOF and return the boundaries for STDEV
- User can output the available arguments for each model so they know what they are able to work with
- User is able to return the parameters of each model after they have been set. 


##### Cleaning With Respect To Taxonomy
```python
import pandas as pd
import numpy as np
import altair as alt
from pandas.core.indexes.numeric import Int64Index

from out_detect_class import Outlier_Detection_DRL
from sklearn.utils.random import sample_without_replacement as swr
# Import data and sample
data = pd.read_csv('initial.csv',usecols=['price','taxonomy'])
index = swr(7999999,200000,random_state = 42)
sample1 = data.iloc[index].reset_index()
# clean data
tune_group = Outlier_Detection_DRL(data = sample1,outlier_column='price',group_column='taxonomy')
clean = tune_group.clean_data()
```
##### Cleaning WithOUT Respect To Taxonomy
```python
import pandas as pd
import numpy as np
import altair as alt
from pandas.core.indexes.numeric import Int64Index

from out_detect_class import Outlier_Detection_DRL
from sklearn.utils.random import sample_without_replacement as swr
# Import data and sample
data = pd.read_csv('initial.csv',usecols=['price','taxonomy'])
index = swr(7999999,200000,random_state = 42)
sample1 = data.iloc[index].reset_index()
# clean data
tune_group = Outlier_Detection_DRL(data = sample1,outlier_column='price')
clean = tune_group.clean_data()
```



