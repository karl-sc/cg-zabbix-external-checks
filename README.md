# cg-zabbix-external-checks
A script to function as Zabbix external checks for WAN utilization, capacity, and App Transaction statistics

### script to be ran in intervals for reporting purposes
### cg-zabbix-check.py [action] [param1] [param2] [param3] [param3]
###  Look at the specific actions for parameters and definitions
### Set a param to 0 to ignore it

All actions give you data for the past 15 minutes and are designed to be ran in that interval.

**** IMPORTANT. Populate the auth_token =  line with your AUTH TOKEN from the CGX portal ****

# Actions:

## wancapacity
- param1 - Site_ID. Unique Site ID number for the site to filter on
- param2 - Circuit Name. Name of Circuit to perform measurement on
- param3 - Direction. Must be either 'ingress' or 'egress'. Which direction of measurement to look at.

Returns the average past 15 minute average of WAN Capacity Measurement using the CGX PCM Data

## wanutilization
- param1 - Site_ID. Unique Site ID number for the site to filter on
- param2 - Circuit Name. Name of Circuit to perform measurement on
- param3 - Direction. Must be either 'ingress' or 'egress'. Which direction of measurement to look at.

Returns the average past 15 minute average of WAN Utilization for a given circuit


## bwutilization
- param1 - Site_ID. Unique Site ID number for the site to filter on. Set to 0 for ALL sites
- param2 - App_Name. Friendly name of Circuit to perform measurement on. Set to 0 for ALL apps. Case Sensitive.

Returns the average past 15 minute per site (optional), per app (optional) Utilization based on the input filters


## appstats
- param1 - Site_ID. Unique Site ID number for the site to filter on. Set to 0 for ALL sites
- param2 - App_Name. Friendly name of Circuit to perform measurement on. Set to 0 for ALL apps. Case Sensitive.
- param3 - Measurement. Must be either 'AppSuccessfulConnections', 'AppSuccessfulTransactions', 'AppFailedToEstablish', or 'AppTransactionFailures'

Returns the average past 15 minute per site (optional), per app (optional) L7 measurement of 'AppSuccessfulConnections', 'AppSuccessfulTransactions', 'AppFailedToEstablish', or 'AppTransactionFailures' based on the input filters


## appresponse
- param1 - Site_ID. Unique Site ID number for the site to filter on. Required.
- param2 - App_Name. Friendly name of Circuit to perform measurement on. Required. Case Sensitive.
- param3 - Measurement. Must be either 'NTT', 'RTT', 'SRT', or 'UDPTRT'

Returns the average past 15 minute per site and per app L7 measurement of 'AppNormalizedNetworkTransferTime', 'AppRoundTripTime', 'AppServerResponseTime', or 'AppUDPTransactionResponseTime' based on the input filters. Note that unlike other queries, 0 may not be used for site-id or app_name.


