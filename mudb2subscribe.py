from shadowsocks import common
import json
import base64
from configloader import load_config, get_config


class Mudb2Sub(object):
    def __init__(self):
        self.config_path = get_config().MUDB_FILE
        self.server_addr = get_config().SERVER_PUB_ADDR
        self.subscribe_file_path = "rss.txt"
        self.json = None
        self.load(self.config_path)

    def load(self, path):
		l = "[]"
		try:
			with open(path, 'rb+') as f:
				l = f.read().decode('utf8')
		except:
			pass
		self.json = json.loads(l)
    
    def ssr_link(self,user,encode):
        protocol = user.get('protocol', '')
        obfs = user.get('obfs', '')
        protocol = protocol.replace("_compatible", "")
        obfs = obfs.replace("_compatible", "")
        protocol_param = user.get('protocol_param', '')
        obfs_param  = user.get('obfs_param', '')
        remarks= user.get('user','')
        isFirstParam = True
        # the params named group must existed in android ssr 
        _group = "HelloWorld"
        params = "/?group="+ common.to_str(base64.urlsafe_b64encode(common.to_bytes(_group))).replace("=", "")
        if protocol_param:
            protocol_param = "protoparam="+ common.to_str(base64.urlsafe_b64encode(common.to_bytes(protocol_param))).replace("=", "")
            params = params +"&"+ protocol_param
        if obfs_param:
            obfs_param = "obfsparam="+ common.to_str(base64.urlsafe_b64encode(common.to_bytes(obfs_param))).replace("=", "")
            params = params +"&"+ obfs_param
        if remarks:
            remarks = "remarks="+ common.to_str(base64.urlsafe_b64encode(common.to_bytes(remarks))).replace("=", "")
            params = params +"&"+ remarks
        link = ("%s:%s:%s:%s:%s:%s"%(self.server_addr,user['port'],protocol,user['method'],obfs,common.to_str(base64.urlsafe_b64encode(common.to_bytes(user['passwd']))).replace("=","")))+params
        return "ssr://" + (encode and common.to_str(base64.urlsafe_b64encode(common.to_bytes(link))).replace("=", "") or link)

    def list_users_ssr(self):
        for user in self.json:
            link = self.ssr_link(user,False)
            print(link)

    def get_subscribe(self):
        result = ''
        for user in self.json:
            result = result+self.ssr_link(user,True)+"\n"
        result_base64 = common.to_str(base64.urlsafe_b64encode(common.to_bytes(result)))
        return result_base64
    
    def gen_subscribe_file(self,result_base64):
        with open(self.subscribe_file_path, 'w') as f:
            f.write(result_base64)

def main():
    manage = Mudb2Sub()
    manage.list_users_ssr()
    result_base64 = manage.get_subscribe()
    manage.gen_subscribe_file(result_base64)

if __name__ == '__main__':
	main()
