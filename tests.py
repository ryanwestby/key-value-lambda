import requests, json

url = 'https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key'
data = {
    "key": "sports",
    "value": "baseball"
  }
auth_header = {'content-type': 'application/json'}


# Test create
post_request = requests.post(
    url,
    data=json.dumps(data),
    headers=auth_header
)

if post_request.status_code == 200:
    print("Create test success: " + post_request.content)
else:
    print("Create test failed: " + str(post_request.status_code) + " " + post_request.content)


# Test list
list_request = requests.get(
    url,
    headers=auth_header
)

if list_request.status_code == 200:
    print("List test success: " + list_request.content)
else:
    print("List test failed: " + str(list_request.status_code) + " " + list_request.content)


# Test update
update_request = requests.put(
    url+'/'+data["key"],
    data=json.dumps({
        "value": '["baseball", "hockey", "football"]'
    }),
    headers=auth_header
)

if update_request.status_code == 200:
    print("Update test success: " + update_request.content)
else:
    print("Update test failed: " + str(update_request.status_code) + " " + update_request.content)


# Test get
get_request = requests.get(
    url+'/'+data["key"],
    headers=auth_header
)

if get_request.status_code == 200:
    print("Get test success: " + json.loads(get_request.content))
else:
    print("Get test failed: " + str(get_request.status_code) + " " + get_request.content)


# Test delete
delete_request = requests.delete(
    url+'/'+data['key'],
    headers=auth_header
)

if delete_request.status_code == 200:
    list_request = requests.get(
        url,
        headers=auth_header
    )
    print("Delete test success: " + list_request.content)
else:
    print("Delete test failed: " + str(delete_request.status_code))
