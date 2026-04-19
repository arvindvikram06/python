from core.plugin_manager import PluginManager

def main():
    print("=== Application Startup ===")

    manager = PluginManager()

    manager.load_plugins("plugins")      
    manager.activate_all()      

    print("[CORE] System ready")

if __name__ == "__main__":
    main()