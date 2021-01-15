### script to be ran in intervals for reporting purposes
### cg-zabbix-check.py [action] [param1] [param2] [param3] [param3]
###  Look at the specific actions for parameters and definitions
### Set a param to 0 to ignore it


### IMPORTANT. Populate the below line with your AUTH TOKEN from the CGX portal
auth_token = ''


def get_wan_path_from_name(sdk, site_id, wan_name):
    try:
        wan_paths = sdk.get.waninterfaces(site_id).cgx_content.get("items")
        for path in wan_paths:
            if path['name'] == wan_name:
                return path['id']
        return None
    except:
        return None

def get_app_id_from_name(sdk, app_name):
    try:
        apps = sdk.get.appdefs().cgx_content.get("items")
        for app in apps:
            if app['display_name'] == app_name:
                return app['id']
        return None
    except:
        return None

def average_series(metrics_series_structure):
    count = 0
    sum = 0
    for datapoints in metrics_series_structure.get("data",[{}])[0].get("datapoints",[{}]):
        if isinstance(datapoints,dict) and (datapoints.get("value",None) is not None):
            count += 1
            sum += datapoints.get("value",0)
        if isinstance(datapoints,list) and (datapoints[0].get("value",None) is not None):
            count += 1
            sum += datapoints.get("value",0)
    if count != 0:
        return sum/count
    return 0

def main():
    try:
        import sys
        action = sys.argv[1]

        from cloudgenix import API
        sdk = API()
        sdk.interactive.use_token(auth_token)

        from datetime import timedelta
        from datetime import datetime
        
        false = False
        true = True
        null = None
        
        end_time = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        

        if action == "wancapacity":
            ### Parameters:     site_id     circuit_name
            ### Interval 15 mins
            
            site_id = sys.argv[2]  # Site_ID
            wan_name = sys.argv[3] ## Circuit Name
            ingress_egress = sys.argv[4] ### Ingress or Egress
            
            wan_path = get_wan_path_from_name(sdk, site_id, wan_name)
            interval = .25  ###15 minutes
            end_time = datetime.now().isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
            start_time = (datetime.now() - timedelta(hours=(interval))).isoformat() 

            post_data = {"start_time": str(start_time) + "Z" ,"end_time": str(end_time) + "Z", 
                        "interval":"10sec","view":
                        {"summary":false, "individual":"direction"},
                        "filter":{"site":[ str(site_id)],"path":[str(wan_path)]},"metrics":[
                        {"name":"PathCapacity","statistics":["average"],"unit":"Mbps"}]}

            metrics = sdk.post.metrics_monitor(post_data).cgx_content
            
            for series in metrics.get("metrics",[{}])[0].get("series",[]):
                if str(ingress_egress).lower() in str(series.get('view',{})).lower():
                    return average_series(series)
            return None
        elif action == "wanutilization":
            ### Parameters:     site_id     circuit_name
            ### Interval 15 mins
            site_id = sys.argv[2]  # Site_ID
            wan_name = sys.argv[3] ## Circuit Name
            ingress_egress = sys.argv[4] ### Ingress or Egress

            wan_path = get_wan_path_from_name(sdk, site_id, wan_name)
            interval = .25  ###15 minutes
            end_time = datetime.now().isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
            start_time = (datetime.now() - timedelta(hours=(interval))).isoformat() 

            post_data = {"start_time": str(start_time) + "Z" ,"end_time": str(end_time) + "Z", 
                        "interval":"10sec","view":
                        {"summary":false, "individual":"direction"},
                        "filter":{"site":[ str(site_id)],"path":[str(wan_path)]},"metrics":[
                            {"name":"BandwidthUsage","statistics":["average"],"unit":"Mbps"}
                        ]}
            metrics = sdk.post.metrics_monitor(post_data).cgx_content
            for series in metrics.get("metrics",[{}])[0].get("series",[{}]):
                if str(ingress_egress).lower() in str(series.get('view',{})).lower():
                    return average_series(series)
        elif action == "bwutilization":
            ### Parameters:     site_id     circuit_name
            ### Interval 15 mins
            site_id = sys.argv[2]  # Site_ID set to 0 for all sites
            app_name = sys.argv[3] ## App Name
            app_id  = "0"
            if app_name != "0":
                app_id  = get_app_id_from_name(sdk, app_name)
            
            interval = .25  ###15 minutes
            end_time = datetime.now().isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
            start_time = (datetime.now() - timedelta(hours=(interval))).isoformat() 


            post_data = {"start_time": str(start_time) + "Z" ,"end_time": str(end_time) + "Z", 
                        "interval":"1min","metrics":
                            [{"name":"BandwidthUsage","statistics":["average"],"unit":"Mbps"} ],"view":{},
                            "filter":{ 
                            "path_type":["DirectInternet","VPN","PrivateVPN","PrivateWAN","ServiceLink"]}}
            if site_id != 0:
                post_data['filter']['site'] = [ str(site_id) ]
            if app_id != 0:
                post_data['filter']['app'] = [ str(app_id) ]
            metrics = sdk.post.metrics_monitor(post_data).cgx_content
            for series in metrics.get("metrics",[{}])[0].get("series",[{}]):
                return average_series(series)
        elif action == "appstats":
            ### Parameters:     site_id     circuit_name
            ### Interval 15 mins
            site_id = sys.argv[2]  # Site_ID set to 0 for all sites
            app_name = sys.argv[3] ## App Name
            measurement = sys.argv[4]
            app_id = "0"
            if app_name != "0":
                app_id  = get_app_id_from_name(sdk, app_name)
            interval = .25  ###15 minutes
            end_time = datetime.now().isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
            start_time = (datetime.now() - timedelta(hours=(interval))).isoformat() 

            post_data = {"start_time": str(start_time) + "Z" ,"end_time": str(end_time) + "Z", 
                        "interval":"10sec",
                        "metrics":[
                            {"name":"AppSuccessfulConnections","statistics":["sum"],"unit":"count"},
                            {"name":"AppSuccessfulTransactions","statistics":["sum"],"unit":"count"},
                            {"name":"AppFailedToEstablish","statistics":["sum"],"unit":"count"},
                            {"name":"AppTransactionFailures","statistics":["sum"],"unit":"count"}],
                        "view":{},"filter":{}}
            if site_id != "0":
                post_data['filter']['site'] = [ str(site_id) ]
            if app_id != "0":
                post_data['filter']['app'] = [ str(app_id) ]
            metrics = sdk.post.metrics_monitor(post_data).cgx_content
            
            for series in metrics.get("metrics",[{}]):
                if str(measurement).lower() in str(series.get("series",[{}])[0].get('name',{})).lower():
                    return( average_series( series.get("series")[0] ))
            return None
        else:
            return None
    except:
        return None


result = main()
if result: print(result) 
