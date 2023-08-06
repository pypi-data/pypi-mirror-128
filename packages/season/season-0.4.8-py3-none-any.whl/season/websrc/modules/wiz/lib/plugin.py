import abc
import datetime
import git
import os

class App:
    def __init__(self, wiz):
        framework = self.framework = wiz.framework

    def __load__(self, data, fs):
        def readfile(key, filename, default=""):
            try:
                data[key] = fs.read(filename)
            except:
                data[key] = default
            return data

        data = readfile("controller", "controller.py")
        data = readfile("api", "api.py")
        data = readfile("socketio", "socketio.py")
        data = readfile("html", "html.dat")
        data = readfile("js", "js.dat")
        data = readfile("css", "css.dat")

        return data    

    def __update__(self, data, fs):
        # check required data
        required = ['controller', 'api', 'socketio', 'html', 'js', 'css']
        for key in required:
            if key not in data: 
                raise Exception(f"wiz plugin: '`{key}`' not defined")

        # save data
        fs.write("controller.py", data['controller'])
        fs.write("api.py", data['api'])
        fs.write("socketio.py", data['socketio'])
        fs.write("html.dat", data['html'])
        fs.write("js.dat", data['js'])
        fs.write("css.dat", data['css'])
    
    """ API Methods
    """
    def pluginpath(self, name=None):
        if name is None:
            return "wiz/plugin"
        return f"wiz/plugin/{name}/apps"

    def load(self, app_id, code=True):
        plugin_name = app_id.split(".")[0]
        fs = self.framework.model("wizfs", module="wiz").use(os.path.join(self.pluginpath(plugin_name), app_id))

        # load app package data
        app = dict()
        app["package"] = fs.read_json(f"app.json")
        try: app["dic"] = fs.read_json(f"dic.json")
        except: app["dic"] = {}

        # if require code data
        if code:
            return self.__load__(app, fs)

        return app

    def update(self, data):        
        # check required attributes
        required = ['package', 'dic']
        for key in required:
            if key not in data: 
                raise Exception(f"wiz app: '`{key}`' not defined")

        required = ['id']
        for key in required:
            if key not in data['package']: 
                raise Exception(f"wiz app: '`package.{key}`' not defined")

        # set timestamp
        package = data['package']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'created' not in package:
            package['created'] = timestamp
        package['updated'] = timestamp
        data['package'] = package

        app_id = package['id']
        plugin_name = app_id.split(".")[0]

        allowed = "qwertyuiopasdfghjklzxcvbnm.-_1234567890"
        for ns in app_id:
            if ns not in allowed:
                raise Exception(f"wiz app: only alphabet and number and -, _ in app_id")
        
        fs = self.framework.model("wizfs", module="wiz").use(os.path.join(self.pluginpath(plugin_name), app_id))

        fs.write_json("app.json", data['package'])
        fs.write_json("dic.json", data['dic'])

        self.__update__(data, fs)

        return self
    
    def delete(self, app_id):
        data = self.get(app_id)
        if data is None:
            return self

        app_id = data['package']['id']
        plugin_name = app_id.split(".")[0]
        if len(app_id) == 0:
            return self

        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath(plugin_name))
        fs.delete(app_id)
        
        return self

    def get(self, app_id):
        try:
            plugin_name = app_id.split(".")[0]
            fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath(plugin_name))
            
            # if app_id exists in route
            if fs.isfile(f"{app_id}/app.json"):
                return self.load(app_id)
        except:
            pass
        return None
    
    def rows(self, plugin_name, full=False):
        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath(plugin_name))
        routes = fs.files()
        res = []
        for app_id in routes:
            if fs.isfile(f"{app_id}/app.json"):
                res.append(self.load(app_id, full))

        res.sort(key=lambda x: x['package']['namespace'])
        return res

    def dic(self, app_id):
        plugin_name = app_id.split(".")[0]
        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath(plugin_name))
        return fs.read_json(f"{app_id}/dic.json")

    def plugin_list(self):
        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath())
        plugins = fs.files()
        res = []
        for plugin_name in plugins:
            try:
                if fs.isdir(plugin_name):
                    res.append(fs.read_json(f"{plugin_name}/wiz-plugin.json"))
            except:
                pass
        return res
    
    def delete_plugin(self, plugin_name):
        if plugin_name is None:
            return self
        if len(plugin_name) == 0:
            return self
        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath())
        fs.delete(plugin_name)
        return self

    def create_plugin(self, plugin_info):
        if 'id' not in plugin_info:
            raise Exception("Plugin id not defined")
        if len(plugin_info['id']) == 0:
            raise Exception("Plugin id not defined")

        plugin_name = plugin_info['id'].lower()

        allowed = "qwertyuiopasdfghjklzxcvbnm-_1234567890"
        for ns in plugin_name:
            if ns not in allowed:
                raise Exception(f"wiz plugin: only alphabet and number and -, _ in plugin")
        
        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath())        
        print(fs.abspath(plugin_name))

        fs.makedirs(plugin_name)

        fs.write_json(f"{plugin_name}/wiz-plugin.json", plugin_info)

    def plugin_info(self, plugin_name):
        fs = self.framework.model("wizfs", module="wiz").use(self.pluginpath(plugin_name))
        return fs.read_json("wiz-plugin.json")