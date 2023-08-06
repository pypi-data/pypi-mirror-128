import requests,mock,json
r='hello'
e='xllo'
n=len(e)
for i in range(len(r)):
    if r[i:i+n]==e:
        print(i)
    else:
        print(-1)

x={'data':[
    []
]}
url='http://hro.test-api.qqxb.jinsehuaqin.com:8800/public/model/w_site_tab_group/list'
head={'Content-Type':'application/json'}
pa={"name":"anonymous_site_list","item_index":0,"item_size":100,"prefilters":[],"columns":["*"],"order_obj":{},"filters":{"date_filters":[],"datetime_filters":[],"text_filters":[],"combo_text_filters":[],"date_between_filters":[],"number_filters":[],"search_filters":[],"boolean_filters":[],"enum_filters":[],"cascader_filters":[],"full_text_filters":[],"combine_full_text_filters":[],"tree_filters":[],"workflow_process_name_filters":[],"workflow_instance_state_filters":[],"simple_relationship_filters":[],"workflow_process_name_multi_filters":[]},"tagFilters":[],"sorts":[]}

pa=json.dumps(pa)
pa={'a':pa}
r=requests.get(url=url,params=pa,headers=head)
print(r.json())