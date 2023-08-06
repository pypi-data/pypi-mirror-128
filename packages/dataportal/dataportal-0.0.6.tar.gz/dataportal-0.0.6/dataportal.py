import urllib.request
import urllib.parse as urlparse
import requests
import xmltodict

class DataportalApi():
    '''
    공공데이터포털 api에서 데이터를 다운로드.
    
    parameters
    ----------
    url : (str) operation명을 뺀 api url
    serviceKey : (str) 공공데이터포털 서비스키
    operation : (str) operation 이름
    params : (dict) parameters of api
    
    returns
    -------
    pd.DataFrame filled with data
    
    
    examples
    --------
    사용 예시 : 기상청 일기도 api
    
    url = 'http://apis.data.go.kr/1360000/WthrChartInfoService'
    serviceKey = 'Test'
    operation = 'getSurfaceChart'
    params = {'code' : 12, 'time' : '20211118'}
    
    dataportal = DataportalApi(url, serviceKey, operation, params)
    response = dataportal.get_request_query()
    api_out = dataportal.parse_response()
    print(api_out)
    
    or you can just do 
    
    dataportal = DataportalApi(url, serviceKey, operation, params)
    api_out = dataportal.load(verbose=False)
    print(api_out)
    
    
    
    '''
    def __init__(self, url,serviceKey, operation, params):
        self.url = url
        self.serviceKey = serviceKey
        self.operation = operation
        self.params = params
        self.response = None
        self.api_out = None

    def get_request_query(self):
        '''
        사용자 request를 받는 함수
        '''
        params = urlparse.urlencode(self.params)
        request_query = f'{self.url}/{self.operation}?serviceKey={self.serviceKey}&{params}'
        self.response = requests.get(url = request_query)
    
    def parse_response(self):
        if (self.response.ok) & (self.response.headers["content-type"].strip().startswith('application/xml')):
            content = self.response.content
            self.api_out = xmltodict.parse(content)['response']
            
        elif (self.response.ok) & (self.response.headers["content-type"].strip().startswith('application/json')):
            content = self.response.content
            self.api_out = content['response']['body']
        
        return self.api_out
    
    def load(self, verbose=False):
        if verbose:
            DataportalApi.get_request_query(self)
            print('get_request_query...')
            api_out = DataportalApi.parse_response(self)
            print('parse_response...')
            print('Done!')
            
        else:
            DataportalApi.get_request_query(self)
            api_out = DataportalApi.parse_response(self)
        
        return api_out

if __name__ == '__main__':

    url = 'http://apis.data.go.kr/1360000/WthrChartInfoService'
    serviceKey = 'Test'
    operation = 'getSurfaceChart'
    params = {'code' : 12, 'time' : '20211118'}
    
    dataportal = DataportalApi(url, serviceKey, operation, params)
    dataportal.get_request_query(operation, params)
    api_out = dataportal.parse_response()
    print(api_out.head())
    
    dataportal = DataportalApi(url, serviceKey, operation, params)
    api_out = dataportal.load(verbose=False)
    print(api_out.head())