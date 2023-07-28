import subprocess as sp

class aira2cc():
    
    class ConfigDictTypeError(Exception):
        def __init__(self,config):
            self.config = config
        def __str__(self):
            print(f"请检查是否对{self.config}参数传入了规定的类型")
    
    def __init__(self,aira_path,aira_cmdoptions=[''],aira_name="aira2c",enable_log_file="aira2c_log.txt",max_concurrent_downloads=5,split=8,enable_check="true",enable_http_proxy=False,checksum=False,timeout=60,max_connection_per_server=1,max_try_times=10,retry_wait_sec=2,min_split_size=1,):
        self.aira_path = aira_path
        self.aira_name = aira_name
        self.aira_cmdoptions = aira_cmdoptions
        included_options = [
            f"--log={enable_log_file}",
            f"--max-concurrent-downloads={max_concurrent_downloads}",
            f"--split={split}",
            f"--connect-timeout={timeout}",
            f"--dry_run={dry_run}",
            f"--max-connection-per-server={max_connection_per_server}",
            f"--max-tries={max_try_times}",
            f"--min-split-siz={min_split_size}",
            f"--retry-wait={retry_wait_sec}",
            f"--timeout={timeout}",
        ]
        '''
        PROXY Dictionary EXAMPLE
        {
            "host":"127.0.0.1",
            "port":"7890",
            "user":"",
            "passwd":"",
        }
        
        SUMCHECK Dictionary EXAMPLE
        {
            "method":"sha-1",
            "sum":""
        }
        '''
        if enable_http_proxy != False:
            if type(enable_http_proxy) == "dict":
                user = enable_http_proxy["user"]
                passwd = enable_http_proxy["passwd"]
                host = enable_http_proxy["host"]
                port = enable_http_proxy["port"]
                proxy = f"--http-proxy={user}:{passwd}@{host}:{port}"
                included_options.append(proxy)
            else:
                raise ConfigDictTypeError("Enable_http_proxy")
            
        if enable_check != False:
            if type(enable_check) == "dict":
                pass
            else:
                raise ConfigDictTypeError("Enable_sumcheck")
    
    def start(self,download_name,download_path,download_url,download_opti=[''],dry_run=False):
        if download_opti == '':
            download_opti = self.aira_cmdoptions
        download_opti += self.included_options
    
    def check(self,):
        pass
    
    def stop(self,):
        pass