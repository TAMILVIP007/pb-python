import requests

class Pandorabots:
    def __init__(self, user_key, app_id, host, botname=False, botkey=False):
        self.user_key = user_key
        self.app_id = app_id
        self.host = host
        self.botname = botname
        self.no_botname_error = {'error':'please set a botname via select_bot("your_botname")'}
        self.no_message_error = {'error':'please include a message string input to your bot, ex. {"message":"hello"}")'}
        self.no_botkey_error = {'error':'please set a botkey via set_botkey("your_botkey")'}
        self.use_api_host_error = {'error':'host must be "api.pandorabots.com" to use atalk with a botkey'}
        self.botkey = botkey
        
    def set_botkey(self, botkey):
        self.botkey = botkey

    def select_bot(self, botname):
        self.botname = botname

    def create_bot(self, botname):
        path = f'/bot/{self.app_id}/{self.botname}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        response = requests.put(url, params=query)
        if response.ok :
            self.botname = botname
        return response
    
    def list_bots(self):
        path = f'/bot/{self.app_id}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        return requests.get(url, params=query)

    def delete_bot(self, botname):
        path = f'/bot/{self.app_id}/{self.botname}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        return requests.delete(url, params=query)

    def upload_file(self, filename):
        if not self.botname:
            return self.no_botname_error
        path = f'/bot/{self.app_id}/{self.botname}/'
        filepath = filename
        if '/' in filename:
            filename = filename.split('/')[-1]
        file_kind = filename.split('.')[-1]
        if file_kind in ['pdefaults', 'properties']:
            path += file_kind
        if file_kind in ['map', 'set', 'substitution']:
            path += f'{file_kind}/' + filename.split('.')[0]
        if file_kind == 'aiml':
            path += f'file/{filename}'
        if path == f'/bot/{self.app_id}/{self.botname}/':
            return 'File type must be one of the following: substitution, properties, aiml, map, set, or pdefaults'

        url = f"https://{self.host}{path}"
        data = open(filepath,'rb').read()
        query = {"user_key": self.user_key}
        return requests.put(url, params=query, data=data)

    def list_files(self):
        if not self.botname:
            return self.no_botname_error
        path = f'/bot/{self.app_id}/{self.botname}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        return requests.get(url,params=query)
    
    def get_file(self, filename):
        if not self.botname:
            return self.no_botname_error
        path = f'/bot/{self.app_id}/{self.botname}/'
        file_kind = filename.split('.')[-1]
        if file_kind in ['pdefaults', 'properties']:
            path += file_kind
        if file_kind in ['map', 'set', 'substitution']:
            path += f'{file_kind}/' + filename.split('.')[0]
        if file_kind == 'aiml':
            path += f'file/{filename}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        return requests.get(url, params=query)
    
    def download_bot(self):
        if not self.botname:
            return self.no_botname_error
        path = f'/bot/{self.app_id}/{self.botname}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key,
                 "return": 'zip'}
        return requests.get(url, params=query)

    def delete_file(self, filename):
        if not self.botname:
            return self.no_botname_error
        path = f'/bot/{self.app_id}/{self.botname}/'
        file_kind = filename.split('.')[-1]
        if file_kind in ['pdefaults', 'properties']:
            path += file_kind
        if file_kind in ['map', 'set', 'substitution']:
            path += f'{file_kind}/' + filename.split('.')[0]
        if file_kind == 'aiml':
            path += f'file/{filename}'
        if path == f'/bot/{self.app_id}/{self.botname}/':
            return 'File type must be one of the following: substitution, properties, aiml, map, set, or pdefaults'

        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        return requests.delete(url, params=query)

    def compile_bot(self):
        if not self.botname:
            return self.no_botname_error
        path = f'/bot/{self.app_id}/{self.botname}/verify'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        return requests.get(url, params=query)

    def talk(self, input, usebotkey=False):
        if (usebotkey and not self.botkey) :
            return self.no_botkey_error
        if usebotkey and self.host != 'api.pandorabots.com':
            return self.use_api_host_error
        if not usebotkey and not self.botname:
            return self.no_botname_error
        if 'message' not in input:
            return self.no_message_error
        path = '/atalk'
        if (not usebotkey):
            path += f'/{self.app_id}/{self.botname}'
        url = f"https://{self.host}{path}"
        query = {"user_key": self.user_key}
        if usebotkey:
            query['botkey'] = self.botkey
        else:
            query["user_key"] = self.user_key
        if 'sessionid' in input:
            query['sessionid'] = input['sessionid']
        if 'recent' in input: 
            query['recent'] = str(input['recent'])
        if 'reset' in input:
            query['reset'] = str(input['reset'])
        if 'trace' in input:
            query['trace'] = str(input['trace'])
        if 'client_name' in input:
            query['client_name'] = input['client_name']
        if 'that' in input:
            query['that'] = input['that']
        if 'topic' in input:
            query['topic'] = input['topic']
        if 'reload' in input:
            query['reload'] = str(input['reload'])
        if 'extra' in input:
            query['extra'] = str(input['extra'])
        return requests.post(url, params=query)
    
    def atalk(self, input, usebotkey=False):
        if (usebotkey and not self.botkey) :
            return self.no_botkey_error
        if usebotkey and self.host != 'api.pandorabots.com':
            return self.use_api_host_error
        if not usebotkey and not self.botname:
            return self.no_botname_error
        if 'message' not in input:
            return self.no_message_error
        path = '/atalk'
        if (not usebotkey):
            path += f'/{self.app_id}/{self.botname}'
        url = f"https://{self.host}{path}"
        query = {"input": input['message']}
        if usebotkey:
            query['botkey'] = self.botkey
        else:
            query["user_key"] = self.user_key
        if 'sessionid' in input:
            query['sessionid'] = input['sessionid']
        if 'recent' in input: 
            query['recent'] = str(input['recent'])
        if 'client_name' in input:
            query['client_name'] = input['client_name']
        return requests.post(url, params=query)
