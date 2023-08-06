import argparse
import os
import re
import shutil

import grpc_tools.protoc

from . import __version__

PACKAGE_PREFIX = "v2ray.com/core"

PROXYMAN = "v2ray.com/core/app/proxyman/command/command.proto"
PROXYMAN_OUT = "v2ray.com/core/app/proxyman/command/command_pb2_grpc.py"

STATS = "v2ray.com/core/app/stats/command/command.proto"
STATS_OUT = "v2ray.com/core/app/stats/command/command_pb2_grpc.py"

IMPORT_REG = re.compile(r"import \"(.+)\";")
OUT = "v2grpc"


class Gen:
    def __init__(self, v2ray_path: str, work_dir: str):
        self._v2ray_path = os.path.abspath(os.path.expanduser(v2ray_path))
        self._work_dir = os.path.abspath(os.path.expanduser(work_dir))

        self._exist = set()
        self._protos = []

        self._grpc_out = os.path.join(self._work_dir, OUT)
        os.makedirs(self._grpc_out, mode=0o755, exist_ok=True)

    def generate(self):
        base_len = len(self._v2ray_path.split(os.sep))
        for root, dirs, files in os.walk(self._v2ray_path):
            for filename in files:
                if filename.endswith(".proto"):
                    src = os.path.join(root, filename)
                    dst = os.path.join(self._work_dir, PACKAGE_PREFIX, *root.split(os.sep)[base_len:])
                    os.makedirs(dst, exist_ok=True)
                    shutil.copy(src, dst)
                    self._protos.append(os.path.join(dst, filename))
        ret = grpc_tools.protoc.main(
            [
                "",
                "--python_out=" + self._grpc_out,
                "--grpc_python_out=" + self._grpc_out,
                "-I",
                self._work_dir,
            ] + self._protos
        )
        self._merge()
        self._cleanup()

    def _merge(self):
        shutil.copyfile(
            os.path.join(self._work_dir, OUT, PROXYMAN_OUT),
            os.path.join(self._work_dir, OUT, "proxyman_pb2_grpc.py")
        )
        shutil.copyfile(
            os.path.join(self._work_dir, OUT, STATS_OUT),
            os.path.join(self._work_dir, OUT, "stats_pb2_grpc.py")
        )
        with open(os.path.join(self._work_dir, OUT, "__init__.py"), "w") as f:
            f.write("""import sys
import os
sys.path.append(os.path.dirname(__file__))
""")

    def _cleanup(self):
        shutil.rmtree(os.path.join(self._work_dir, "v2ray.com"))
        shutil.rmtree(os.path.join(self._work_dir, OUT, "v2ray.com"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", required=True, help="the v2ray source directory")
    parser.add_argument("--output", "-o", default=".", help="set the directory for protoc output, "
                                                            "default is current directory")
    parser.add_argument("--version", "-v", action="version",
                        version=f"version: {__version__}", help="show the version")
    args = parser.parse_args()
    if args.source is None:
        parser.print_help()

    g = Gen(args.source, args.output)
    g.generate()


if __name__ == "__main__":
    main()
