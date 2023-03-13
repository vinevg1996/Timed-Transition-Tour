import subprocess
import shlex
import json
import requests 
import time

device1 = "of:0000000000000001"
device2 = "of:0000000000000002"
app = 666

pattern = ''' curl -u onos:rocks -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '''
url = ''' 'http://localhost:8181/onos/v1/flows?appId=666' '''


payload_for_test = """{
        "flows": [
        {
          "priority": 40000,
          "timeout": 0,
          "isPermanent": false,
          "deviceId": "of:0000000000000001",
          "treatment": {
            "instructions": [
              {
                "type": "OUTPUT",
                "port": "2"
              }
            ]
          },
          "selector": {
            "criteria": [
              {
                "type": "IN_PORT",
                "port": "1"
              },
              {
                "type": "ETH_SRC",
                "mac": "9a:d8:73:d8:90:6a"
              },
              {
                "type": "ETH_DST",
                "mac": "9a:d8:73:d8:90:6b"
              }
            ]
          }
        }
        ]
    }"""

class ONOS_interface:
    def __init__(self):
        self.flow_rules = list()
        return

    def run_curl_cmd(self, cmd):
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        resp = json.loads(stdout.decode('utf-8'))
        return resp

    def delete_rules_from_flow_rules(self):
        delete_str = 'http://localhost:8181/onos/v1/flows/of%3A0000000000000001/'
        for flowId in self.flow_rules:
            delete_str_flowId = delete_str + flowId
            resp = requests.delete(delete_str_flowId, auth=('onos', 'rocks'))
            #print("resp =", resp)
        return

    def get_rules_from_flow_rules(self):
        get_str = 'http://localhost:8181/onos/v1/flows/of%3A0000000000000001/'
        for flowId in self.flow_rules:
            get_str_flowId = get_str + flowId
            resp = requests.get(get_str_flowId, auth=('onos', 'rocks'))
            #print("resp =", resp)
        return

    def add_rules(self, rules_number):
        dummy_payload = """{
            "flows": [
            {
              "priority": 40000,
              "timeout": 0,
              "isPermanent": true,
              "deviceId": "of:0000000000000001",
              "treatment": {
                "instructions": [
                  {
                    "type": "OUTPUT",
                    "port": "2"
                  }
                ]
              },
              "selector": {
                "criteria": [
                  {
                    "type": "IN_PORT",
                    "port": "1"
                  },
                  {
                    "type": "ETH_SRC",
                    "mac": "9a:d8:73:d8:90:6a"
                  },
                  {
                    "type": "ETH_DST",
                    "mac": "9a:d8:73:d8:90:6b"
                  }
                ]
              }
            }
            ]
        }"""
        #time.sleep(2)
        data = json.loads(dummy_payload)
        for i in range(0, rules_number):
            data["flows"][0]['priority'] = 40000 + (i+1)
            json_data_payload = json.dumps(data)
            cmd_dummy_payload = pattern + ''' ' ''' + json_data_payload + ''' ' ''' + str(url)
            resp = self.run_curl_cmd(cmd_dummy_payload)
            self.flow_rules.append(resp['flows'][0]['flowId'])
        return

    def run_test_pf1_pf2(self, t1, timeout1, t2, timeout2):
        dummy_payload = """{
            "flows": [
            {
              "priority": 40000,
              "timeout": 0,
              "isPermanent": false,
              "deviceId": "of:0000000000000001",
              "treatment": {
                "instructions": [
                  {
                    "type": "OUTPUT",
                    "port": "2"
                  }
                ]
              },
              "selector": {
                "criteria": [
                  {
                    "type": "IN_PORT",
                    "port": "1"
                  },
                  {
                    "type": "ETH_SRC",
                    "mac": "9a:d8:73:d8:90:6a"
                  },
                  {
                    "type": "ETH_DST",
                    "mac": "9a:d8:73:d8:90:6b"
                  }
                ]
              }
            }
            ]
        }"""
        data1 = json.loads(dummy_payload)
        data1["flows"][0]['priority'] = 40000 + 1
        data1["flows"][0]['timeout'] = int(timeout1)
        json_data_payload1 = json.dumps(data1)
        cmd_dummy_payload1 = pattern + ''' ' ''' + json_data_payload1 + ''' ' ''' + str(url)
        data2 = json.loads(dummy_payload)
        data2["flows"][0]['priority'] = 40000 + 2
        data2["flows"][0]['timeout'] = int(timeout2)
        json_data_payload2 = json.dumps(data2)
        cmd_dummy_payload2 = pattern + ''' ' ''' + json_data_payload2 + ''' ' ''' + str(url)
        # start_test
        time.sleep(t1)
        resp1 = self.run_curl_cmd(cmd_dummy_payload1)
        time.sleep(t2)
        resp2 = self.run_curl_cmd(cmd_dummy_payload2)
        print("resp1=", resp1)
        print("resp2=", resp2)
        return

    def run_pf1(self, timeout1):
        data1 = json.loads(payload_for_test)
        data1["flows"][0]['priority'] = 40001
        data1["flows"][0]['timeout'] = int(timeout1)
        json_data_payload1 = json.dumps(data1)
        cmd_dummy_payload1 = pattern + ''' ' ''' + json_data_payload1 + ''' ' ''' + str(url)
        resp1 = self.run_curl_cmd(cmd_dummy_payload1)
        return resp1

    def run_pf2(self, timeout2):
        data2 = json.loads(payload_for_test)
        data2["flows"][0]['priority'] = 40002
        data2["flows"][0]['timeout'] = int(timeout2)
        json_data_payload2 = json.dumps(data2)
        cmd_dummy_payload2 = pattern + ''' ' ''' + json_data_payload2 + ''' ' ''' + str(url)
        resp2 = self.run_curl_cmd(cmd_dummy_payload2)
        return resp2

onos = ONOS_interface()
#onos.add_rules(100)
#print(onos.flow_rules)

#time.sleep(1)
start_time = time.time()
#onos.delete_rules_from_flow_rules()
t1 = float(2)
timeout1 = int(5)
t2 = float(2.5)
timeout2 = int(2)
#onos.run_test_pf1_pf2(t1, timeout1, t2, timeout2)

#time.sleep(2.5)

# test1 = (pf1,3),(pf1,6),(pf2,8),(pf1,11),(pf2,13),(pf1,14.5)
# test2 = (pf1,3),(pf2,9),(pf1,12),(pf2,14)
# test3 = (pf2,2),(pf2,4),(pf1,5.5),(pf2,7.5),(pf2,13.5),(pf1,16.5)

time.sleep(2)
onos.run_pf1(5)
time.sleep(2.1)
#onos.run_pf2(2)
onos.run_pf2(3)
print("execution_time =", time.time() - start_time)