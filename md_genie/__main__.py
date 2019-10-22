from md_genie import cli
from md_genie import server

def main():
    args = cli.args
    print(args)
    server.start_server()

if __name__ == "__main__":
    main()
