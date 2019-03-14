from prometheus_client import Gauge 
from wavefront.apis import sendMetric
from metadata.globalconfig import globalconfig
from utils.dictutils import convertDictKey


metric_prefix = "foremastbrain:"
wavefront_prefix='custom.iks.'

globalConfig =  globalconfig()
#globalConfig.getValueByKey('FOREMAST_ENV')

class modelmetrics:
    class __modelmetrics:
        def __init__(self):
            self.metrics = {}
        def __str__(self):
            return repr(self) + self.configs
    instance = None
    def __init__(self):
        if not modelmetrics.instance:
            modelmetrics.instance = modelmetrics.__modelmetrics()
    def setMetricInfo(self, metricname, labels):
        metricNameUpper = metric_prefix+metricname+"_upper"
        metricNameLower = metric_prefix+metricname+"_lower"
        newlabeldata= convertDictKey(labels,"-", "_")
        if not (metricNameUpper in self.instance.metrics ):
            self.instance.metrics[metricNameUpper] = Gauge(metricNameUpper, metricNameUpper+" model upper bound",  
                                                  labelnames=newlabeldata.keys())
        if not (metricNameLower in self.instance.metrics ):
            self.instance.metrics[metricNameLower] = Gauge(metricNameLower, metricNameLower+" model upper bound", 
                                                   labelnames=newlabeldata.keys())                                     
                                                   
    def sendMetric(self,metricname, labeldata, value, isUpper = True, time=0):
        newMetricName = metric_prefix+metricname
        if isUpper:
            newMetricName  += "_upper"
        else:
            newMetricName  += "_lower"
        if globalConfig.getValueByKey('METRIC_DESTINATION')=='wavefront':
            newMetricName  = wavefront_prefix+ newMetricName
            return sendMetric(newMetricName, labeldata, value, time)
        if not (newMetricName in self.instance.metrics) :
                self.setMetricInfo(metricname, labeldata) 
        newlabeldata = convertDictKey(labeldata,"-", "_")
        self.instance.metrics[newMetricName].labels(**newlabeldata).set(value)




class measurementmetrics:
    class __measurementmetrics:
        def __init__(self):
            self.metrics = {}
        def __str__(self):
            return repr(self) + self.configs
    instance = None
    def __init__(self):
        if not measurementmetrics.instance:
            measurementmetrics.instance = measurementmetrics.__measurementmetrics()
    def setMetricInfo(self, metricname, labels):
        newMetricName = metric_prefix+metricname
        newlabeldata= convertDictKey(labels,"-", "_")
        if not (newMetricName in self.instance.metrics ):
            self.instance.metrics[newMetricName] = Gauge(newMetricName, newMetricName+" measurement metric",
                                                           labelnames=newlabeldata.keys())                                                                                    
    def sendMetric(self,metricname, labeldata, value, time=0):
        newMetricName = metric_prefix+metricname
        if globalConfig.getValueByKey('METRIC_DESTINATION')=='wavefront':
            newMetricName =wavefront_prefix + newMetricName
            return sendMetric(newMetricName, labeldata, value, time)
        if not (newMetricName in self.instance.metrics) :
            self.setMetricInfo(metricname, labeldata)             
        newlabeldata = convertDictKey(labeldata,"-", "_")
        self.instance.metrics[newMetricName].labels(**newlabeldata).set(value)


    
    
class anomalymetrics:
    class __anomalymetrics:
        def __init__(self):
            self.metrics = {}
        def __str__(self):
            return repr(self) + self.configs
    instance = None
    def __init__(self):
        if not anomalymetrics.instance:
            anomalymetrics.instance = anomalymetrics.__anomalymetrics()
    def setMetricInfo(self, metricname, labels):
        metricNameAnomaly = metric_prefix+metricname+"_anomaly"
        newlabeldata= convertDictKey(labels,"-", "_")
        if not (metricNameAnomaly in self.instance.metrics ):
            self.instance.metrics[metricNameAnomaly] = Gauge(metricNameAnomaly, metricNameAnomaly+" anomaly timestamp",  
                    labelnames=newlabeldata.keys())                                                                                        
                                                   
    def sendMetric(self,metricname, labeldata, value, time=0):
        newMetricName  = metric_prefix+metricname+"_anomaly"
        if globalConfig.getValueByKey('METRIC_DESTINATION')=='wavefront':
            newMetricName =wavefront_prefix + newMetricName
            return sendMetric(newMetricName, labeldata, value, time) 
        if not (newMetricName in self.instance.metrics ):
            self.setMetricInfo(metricname, labeldata)  
        newlabeldata = convertDictKey(labeldata,"-", "_")         
        self.instance.metrics[newMetricName].labels(**newlabeldata).set(value)
        
        
class hpascoremetrics:
    class __hpascoremetrics:
        def __init__(self):
            self.metrics = {}
        def __str__(self):
            return repr(self) + self.configs
    instance = None
    def __init__(self):
        if not hpascoremetrics.instance:
           hpascoremetrics.instance = hpascoremetrics.__hpascoremetrics()
    def setMetricInfo(self, metricname, labels, time=0):
        mns =metricname.split(':')
        metricHPA = metric_prefix+mns[0]+"_hpa_score"
        if (len(mns)>1):
            metricHPA = metric_prefix+mns[0]+":"+"hpa_score"
        newlabeldata = convertDictKey(labels,"-", "_")
        if not (metricHPA in self.instance.metrics ):
            self.instance.metrics[metricHPA] = Gauge(metricHPA, metricHPA+" hpa score",  
                    labelnames=newlabeldata.keys())                                                                                        
                                                   
    def sendMetric(self,metricname, labeldata, value, time=0):
        mns =metricname.split(':')
        newMetricName= metric_prefix+mns[0]+"_hpa_score"
        if (len(mns)>1):
            newMetricName = metric_prefix+mns[0]+":"+"hpa_score"
        if globalConfig.getValueByKey('METRIC_DESTINATION')=='wavefront':
            newMetricName = wavefront_prefix+ newMetricName
            return sendMetric(newMetricName, labeldata, value, time) 
        if not (newMetricName in self.instance.metrics ):
            self.setMetricInfo(metricname, labeldata)          
        newlabeldata = convertDictKey(labeldata,"-", "_")
        self.instance.metrics[newMetricName].labels(**newlabeldata).set(value)