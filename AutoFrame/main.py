"""
"""
# import gevent
# from gevent import monkey
# monkey.patch_all()
from engine.server import create_app

app = create_app()
# 挂载静态文件目录
# app.mount('/v1/qc/staticfile', StaticFiles(directory=os.path.join(root_dir, 'logs')))
# app.mount(path='/v1/qc/reports/', app=StaticFiles(directory=os.path.join(root_dir, 'logs/automation/reports')))

if __name__ == "__main__":
    # 输出所有路由
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})

    import uvicorn
    uvicorn.run(app='main:app', host="0.0.0.0", port=8080, reload=False)

