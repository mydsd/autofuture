
import os
from scripts.get_ini import GetConfig
base_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
conPath = os.path.join(base_path,'engine', 'conf.ini')

config = GetConfig(conPath).read_ini()

# mode
debug = True

# docs
title = "测试管理"
description = "测试管理后端接口"
docs_url = "/api/docs"
openapi_url = "/api/openapi.json"
redoc_url = "/api/redoc"

# mysql
data_source = config['mysql']['data_source']
