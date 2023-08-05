class API:

    def __init__(self, performance=False):
        self.performance = performance
        self.__result = None
        self.__syntax = None

    @property
    def get_start_class(self):
        if self.performance:
            return f'''from locust import HttpUser, task
        
            
class WebsiteUser(HttpUser):
        
        '''
        else:
            return '''
import allure
import api
'''

    @property
    def get_headers_example(self):
        return str({'Content-Type': 'application/json', 'Accept': 'application/json'})

    @property
    def get_params_example(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}

    @property
    def get_body_example(self):
        return {
            "jsonObject": {
                "type1": "MultiPolygon1",
                "typ2": "MultiPolygon2",
            }
        }

    @property
    def expected_status_code_method(self):
        return """
        
@allure.step("Expected Status Code")
def analyze_response(res, expected_status_code):
    if res.status_code != expected_status_code:
        assert False
    else:
        print(f"status code is {res.status_code}")"""

    def set_method(self, method, resource, params=None, headers=None, body=None, name='service_1', domain=None):
        if self.performance:
            self.__syntax = f"self.client.{method}(url='{resource}'"
        else:
            self.__syntax = f"""   
@allure.feature("Set Feature For {name}")
@allure.description("Set Description For {name}")        
def test_{name}():
    component_{name}()

@allure.step("Set Step Description For {name}")
def component_{name}():
     api_instance = api.rest_api.ApiCapabilities()
     response = api_instance.{method}_request(url='{domain}{resource}?'"""
        if params is not None and len(params) > 0:
            self.__syntax += f", params={params}"

        if headers is not None and len(headers) > 0:
            self.__syntax += f", headers={headers}"

        if body is not None and len(body) > 0:
            self.__syntax += f", data={body}"

        if self.performance:
            self.__result = f'''
        @task
        def {name}(self):
            {self.__syntax})'''

        else:
            self.__result = f'''
{self.__syntax})
     analyze_response(response, 200)
'''
        return f"{self.__result}"
