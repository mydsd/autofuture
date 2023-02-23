
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from engine import load_conf

# 初始化数据库连接信息
# DB_CONNECT = f'mysql+pymysql://{load_conf.data_user}:{data_password}@{load_conf.data_localhost}?charset=utf8mb4'
# engine = create_engine(DB_CONNECT, pool_pre_ping=True, isolation_level="READ COMMITTED", max_overflow=8, pool_size=50)
engine = create_engine(load_conf.data_source)

# 创建一个配置过的Session类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 实例化一个session
db_session = scoped_session(SessionLocal)

