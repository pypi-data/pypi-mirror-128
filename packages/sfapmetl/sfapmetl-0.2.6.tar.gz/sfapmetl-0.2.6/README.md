#### Python etl feature 

##### Installation
> $ pip install sfapmetl
##### Usage
> $ etl-script <config file path>

Please provide config as mentioned below
```
key: <profile key>
tags: 
  Name: <name>
  appName: <appName>
  projectName: <projectName>
metrics:
  plugins:
    - name: <PluginName>
      enabled: true
      url: <componentUrl>
      authkey: <authentication_key_for_the_url>
```
* After this setup, add cronjob into /etc/crontab( Applicable for Linux AWS instance, else run this script as a cron job) ex: To run script every 5 minutes - */5 * * * * root etl-script <config file path>

* Please refer this link for cronjob https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804

