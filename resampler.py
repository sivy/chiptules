import argparse
import ffmpeg
from pathlib import Path

# one weird trick to remove the extra "encoder" metadata
# that ffmpeg adds and deflemask h8s
one_weird_trick = {
    "map_metadata": -1,
    "fflags": "+bitexact", "flags:v": "+bitexact",
    "flags:a": "+bitexact"
}


def main(args):
    # one file at a time
    if args.infile:
        infile = Path(args.infile)
        outfile = Path(args.outfile)
        run_opts = {"quiet": True}
        if args.debug:
            run_opts = {"quiet": False}
        (
            ffmpeg.input(str(infile))
            .output(str(outfile), ac=1, ar=args.rate, **one_weird_trick)
            .overwrite_output()
            .run(**run_opts)
        )

    elif args.source:
        source = Path(args.source)
        print(source)
        dest = Path(args.outdir)
        if not dest.exists():
            dest.mkdir()

        for f in source.glob("**/*.wav"):
            print(f)
            subp = Path(*f.parts[f.parts.index(source.name) + 1 :])
            print(subp)

            outdir = dest / subp.parent
            outfile = outdir / subp.name
            print(f"outfile: {outfile}")
            (dest / subp.parent).mkdir(exist_ok=True)
            run_opts = {"quiet": True}
            if args.debug:
                run_opts = {"quiet": False}
            (
                ffmpeg.input(str(f))
                .output(str(outfile), ac=1, ar=args.rate, **one_weird_trick)
                .overwrite_output()
                .run(**run_opts)
            )
            # use --test to only run one file in a batch
            # or use --in and --out,  but this is easier for
            # debugging batches
            if args.test:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # processing files
    parser.add_argument("--in", dest="infile")
    parser.add_argument("--out", dest="outfile")
    # processing directories
    parser.add_argument("--source", dest="source")
    parser.add_argument("--dest", dest="destination")
    parser.add_argument("--rate")
    parser.add_argument("--test", action="store_true", default=False)
    # print all the ffmpeg garbage for debugging
    parser.add_argument(
        "--ffmpeg-debug", dest="debug", action="store_true", default=False
    )
    args = parser.parse_args()

    main(args)
