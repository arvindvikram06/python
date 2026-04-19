import argparse
from core.plugin_manager import PluginManager

def main():
    parser = argparse.ArgumentParser(prog="sitegen")
    parser.add_argument("command", choices=["build"])
    parser.add_argument("--theme", default="default")

    args = parser.parse_args()

    print("=== Application Startup ===")
    print(f"$ sitegen {args.command} --theme {args.theme}")

    manager = PluginManager()

    manager.load_plugins()
    manager.resolve_dependencies()
    manager.activate_all()

    if args.command == "build":
        build_site(args.theme)

    manager.deactivate_all()

    print("[CORE] Build complete")

def build_site(theme):
    print("[CORE] Building site...")
    print(f"[CORE] Theme selected: {theme}")
    print("[CORE] Processing pages...")
    print("[CORE] Build finished -> ./dist/")

if __name__ == "__main__":
    main()