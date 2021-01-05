# only support python 3
import http.client
import time
import json

def get_iam_arn():
    
    response = IMDSv1_extracter("iam/info/")
    json_response = json.loads(response)
    arn = json_response["InstanceProfileArn"]
    return(arn)


def IMDSv1_extracter(path=''):
    
    conn = http.client.HTTPConnection('169.254.169.254')
    conn.request("GET", f"/latest/meta-data/{path}")
    response = conn.getresponse()
    time.sleep(1) #To prevent from throttling sleep for 1 second
    conn.close()
    return(response.read())
    

def IMDSv2_extracter():
    
    conn = http.client.HTTPConnection('169.254.169.254')
    conn.request("PUT", "/latest/api/token", headers={"X-aws-ec2-metadata-token-ttl-seconds": 21600})
    response = conn.getresponse()
    print("IMDSv2 PUT token", response.status, response.reason)
    token = response.read()
    time.sleep(1) #To prevent from throttling sleep for 1 second
    
    conn.request("GET", "/latest/meta-data/", headers={"X-aws-ec2-metadata-token": token})
    response = conn.getresponse()
    print("IMDSv2 GET meta-data", response.status, response.reason)
    print(response.read())
    conn.close()


if __name__ == "__main__":
    
    IMDSv1_extracter()
    IMDSv2_extracter()
    
    get_iam_arn()